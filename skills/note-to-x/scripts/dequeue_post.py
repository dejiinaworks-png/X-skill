"""
キュー投稿スクリプト
queue/queue.json の先頭1件を取り出してXに投稿し、キューから削除する。

GitHub Actions から自動実行される。
ローカルでのテスト:
  python skills/note-to-x/scripts/dequeue_post.py --dry-run
"""

import os
import sys
import json
import argparse
import tweepy
from pathlib import Path
from dotenv import load_dotenv

# ルートの .env を読む（ローカル実行時）
ROOT_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

QUEUE_FILE = ROOT_DIR / "queue" / "queue.json"
QUEUE_IMAGES_DIR = ROOT_DIR / "queue" / "images"
POSTED_IDS_FILE = ROOT_DIR / "queue" / "posted_ids.json"


def get_client_v1() -> tweepy.API:
    auth = tweepy.OAuth1UserHandler(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_KEY_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )
    return tweepy.API(auth)


def get_client_v2() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=os.environ["API_KEY"],
        consumer_secret=os.environ["API_KEY_SECRET"],
        access_token=os.environ["ACCESS_TOKEN"],
        access_token_secret=os.environ["ACCESS_TOKEN_SECRET"],
    )


def generate_image(prompt: str, output_path: str) -> bool:
    """Gemini API で画像生成（image_prompt が指定されている場合）"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY 未設定、画像なしで投稿")
        return False

    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["Text", "Image"])
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_bytes(part.inline_data.data)
                print(f"🎨 画像生成完了: {output_path}")
                return True
    except Exception as e:
        print(f"⚠️  画像生成失敗: {e}")
    return False


def post(text: str, image_path: str = None, dry_run: bool = False) -> str:
    """Xに投稿。画像あり/なし両対応。ツイートIDを返す。"""
    if dry_run:
        print(f"[DRY RUN] 投稿（{len(text)}文字）:\n{text}")
        if image_path:
            print(f"[DRY RUN] 画像: {image_path}")
        return "dry_run_id"

    media_ids = None

    if image_path and Path(image_path).exists():
        print(f"📤 画像アップロード: {image_path}")
        api_v1 = get_client_v1()
        media = api_v1.media_upload(filename=image_path)
        media_ids = [media.media_id]
        print(f"   media_id: {media.media_id}")

    client = get_client_v2()
    kwargs = {"text": text}
    if media_ids:
        kwargs["media_ids"] = media_ids

    response = client.create_tweet(**kwargs)
    tweet_id = response.data["id"]
    print(f"✅ 投稿成功: https://x.com/i/web/status/{tweet_id}")
    return tweet_id


def load_posted_ids() -> set:
    """投稿済みIDのセットを読み込む"""
    if not POSTED_IDS_FILE.exists():
        return set()
    with open(POSTED_IDS_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))


def save_posted_id(item_id: str):
    """投稿済みIDを記録する"""
    posted = load_posted_ids()
    posted.add(item_id)
    POSTED_IDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTED_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(posted), f, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="キューから1件取り出して投稿")
    parser.add_argument("--dry-run", action="store_true", help="投稿せず確認のみ")
    args = parser.parse_args()

    # キュー読み込み
    if not QUEUE_FILE.exists():
        print("❌ queue/queue.json が見つかりません")
        sys.exit(1)

    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        queue = json.load(f)

    if not queue:
        print("📭 キューが空です。投稿をスキップ。")
        sys.exit(0)

    # 投稿済みIDを読み込み
    posted_ids = load_posted_ids()

    # 先頭1件を取得（投稿済みはスキップ）
    item = queue[0]
    item_id = item["id"]

    if item_id in posted_ids:
        print(f"⚠️  ID '{item_id}' は投稿済みです（重複防止）。キューから削除します。")
        if not args.dry_run:
            queue.pop(0)
            with open(QUEUE_FILE, "w", encoding="utf-8") as f:
                json.dump(queue, f, ensure_ascii=False, indent=2)
            print(f"🗑️  キューから削除。残り {len(queue)}件")
        sys.exit(0)

    text = item["text"]
    image_path = item.get("image_path")
    image_prompt = item.get("image_prompt")

    print(f"📋 投稿ID: {item_id}")
    print(f"   残りキュー: {len(queue)}件 → 投稿後 {len(queue)-1}件")

    # image_prompt がある場合は画像を生成
    if image_prompt and not image_path:
        gen_path = str(QUEUE_IMAGES_DIR / f"{item_id}.png")
        if generate_image(image_prompt, gen_path):
            image_path = gen_path

    # 投稿
    post(text, image_path=image_path, dry_run=args.dry_run)

    # dry_run でない場合のみキューから削除 & 投稿済みIDを記録
    if not args.dry_run:
        save_posted_id(item_id)
        queue.pop(0)
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print(f"🗑️  キューから削除。残り {len(queue)}件")


if __name__ == "__main__":
    main()
