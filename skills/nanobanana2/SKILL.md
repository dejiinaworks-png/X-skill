# NanoBanana2

Gemini API（`gemini-2.0-flash-preview-image-generation`）で画像を生成するスキル。
ブラウザ操作不要、APIキー1本で動く。

## セットアップ

```bash
pip install -r requirements.txt
```

`.env` に追加:
```
GEMINI_API_KEY=your_key_here
```

APIキー取得: https://aistudio.google.com/apikey

## 使い方

```bash
python skills/nanobanana2/scripts/generate.py \
  --prompt "インフォグラフィック：AI活用術5選、白背景、日本語、シンプル" \
  --output output/image.png
```

## 出力

- PNG画像を指定パスに保存
- X投稿時は tweepy の `media_upload` で添付可能
