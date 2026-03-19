#!/usr/bin/env python3
"""
NanoBanana2 - Gemini API 画像生成スクリプト
gemini-2.0-flash-preview-image-generation を使ってAPIキーで画像生成。

使い方:
    python scripts/generate.py --prompt "プロンプト" --output output/image.png
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# X投稿くんルートの .env を読み込む
ROOT_DIR = Path(__file__).parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-3.1-flash-image-preview"


def generate_image(prompt: str, output_path: str) -> bool:
    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY が .env に未設定")
        print("   https://aistudio.google.com/apikey でキーを取得してください")
        return False

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        print("❌ google-genai 未インストール: pip install google-genai")
        return False

    print(f"🎨 生成中... [{prompt[:50]}]")

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"]
        )
    )

    # 画像パーツを探す
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(part.inline_data.data)
            print(f"✅ 保存: {output_path}")
            return True

    # 画像なし（テキストのみ返ってきた場合）
    for part in response.candidates[0].content.parts:
        if hasattr(part, "text") and part.text:
            print(f"Gemini: {part.text}")
    print("❌ 画像データなし")
    return False


def main():
    parser = argparse.ArgumentParser(description="NanoBanana2: Gemini API 画像生成")
    parser.add_argument("--prompt", required=True, help="画像生成プロンプト")
    parser.add_argument("--output", default="output/generated.png", help="出力パス")
    args = parser.parse_args()

    return 0 if generate_image(args.prompt, args.output) else 1


if __name__ == "__main__":
    sys.exit(main())
