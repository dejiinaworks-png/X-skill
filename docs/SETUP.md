# X API 開通手順

## Step 1: X Developer Portal でアカウント登録

1. https://developer.x.com にアクセス（Xアカウントでログイン）
2. **「Sign up for Free Account」** をクリック
3. 利用目的を **250文字以上** で記述（日本語でも可）

   記述例:
   ```
   I am building a personal tool to automatically post scheduled content
   to my X account using the API. I will use it to convert note.com blog
   articles into tweet-format posts and schedule them for better engagement.
   This is for personal use only and I will comply with all automation rules.
   ```

4. 利用規約に同意 → 承認（通常即座に完了）

---

## Step 2: プロジェクト・アプリ作成

1. ダッシュボード（https://developer.x.com/en/portal/dashboard）へ移動
2. **「+ Create Project」** をクリック
   - Project name: 任意（例: `XSkillProject`）
   - Use case: 「Making a bot」または「Automating posts」
3. **「+ Create App」** をクリック
   - App name: グローバルでユニークな名前（例: `xskill-yourname`）
4. 表示される以下を **必ずコピー保存**（1度しか表示されない）
   - ✅ API Key
   - ✅ API Key Secret
   - ✅ Bearer Token

---

## Step 3: OAuth 権限設定（最重要）

> ⚠️ ここを間違えると 403 エラーが出ます

1. ダッシュボード → 対象アプリ → **「Settings」タブ**
2. 「User authentication settings」の **「Set up」** をクリック
3. 以下を設定:
   - **App permissions**: `Read and Write` ← ここが重要！（デフォルトは Read のみ）
   - **Type of App**: `Web App, Automated App or Bot`
   - **Callback URI**: `http://localhost:8080/callback`
   - **Website URL**: `https://github.com/dejiinaworks-png/X-skill`
4. **「Save」** をクリック

---

## Step 4: Access Token の（再）生成

> ⚠️ Step 3でPermissionsを変更した後は必ず再生成！

1. 「Keys and Tokens」タブへ移動
2. 「Access Token and Secret」の **「Generate」または「Regenerate」** をクリック
3. 表示される以下をコピー保存:
   - ✅ Access Token
   - ✅ Access Token Secret

---

## Step 5: .env ファイルに設定

プロジェクトルートに `.env` ファイルを作成:

```bash
# .env.example をコピー
cp .env.example .env
```

`.env` を開いて5つのキーを入力:

```
API_KEY=取得したAPI Key
API_KEY_SECRET=取得したAPI Key Secret
BEARER_TOKEN=取得したBearer Token
ACCESS_TOKEN=取得したAccess Token
ACCESS_TOKEN_SECRET=取得したAccess Token Secret
```

---

## Step 6: テスト投稿

```bash
# Pythonパッケージをインストール
pip install -r requirements.txt

# テスト投稿（--dry-run で確認のみ）
python skills/note-to-x/scripts/post_to_x.py --dry-run

# 実際に投稿
python skills/note-to-x/scripts/post_to_x.py
```

✅ 成功すると以下のように表示されます:
```
投稿成功!
   ID  : 1234567890
   URL : https://x.com/i/web/status/1234567890
   本文: X-skill 開通テスト ✅
```

---

## よくあるエラー

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `403 Forbidden` | App Permissionsが「Read」のまま | Step 3→4をやり直す |
| `401 Unauthorized` | APIキーが間違っている | .envを確認・コピーミスがないか |
| `402 CreditsDepleted` | 新規アカウントで$5未課金 | Developer Portal でクレジット購入 |
| `429 Too Many Requests` | レート制限超過 | しばらく待つ（自動リトライあり） |

---

## Free Tier の制限

| 項目 | 制限 |
|------|------|
| 月間投稿数 | 500件/月（旧ユーザー）または従量課金 |
| 読み取り | **不可**（書き込み専用） |
| 新規アカウント | $5のクレジット購入が必要な場合あり |
