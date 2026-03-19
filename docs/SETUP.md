# X API 開通手順（2026年版）

> ⚠️ **重要**: 2026年より Free プランが廃止されました。
> **Pay Per Use（従量課金）への登録が必須**です。
> ただし参加時に **$500の無料クレジット**が付与されるため実質無料で始められます。

---

## Step 1: Pay Per Use パイロットに参加する

1. https://developer.x.com にアクセス（Xアカウントでログイン）
2. 左メニュー **Products → X API v2** を開く
3. オレンジのバナー内の **「Pay Per Use」** リンクをクリック
4. 「ペイパーユースパイロットに参加する」画面で：
   - プロジェクト名・説明を入力（例: `X-skills-dejiina`）
   - ユースケース: **「Making a bot」** を選択
5. 参加申請を完了する

> 💡 参加後に **$500の無料クレジット**が付与されます。
> 月100投稿（$0.01/投稿）= $1/月 なので、約40年分相当。

新しいコンソール: https://console.x.com/accounts/

---

## Step 2: プロジェクト・アプリ作成

1. ダッシュボード（https://developer.x.com/en/portal/dashboard）へ移動
2. **「+ Create Project」** をクリック
   - Project name: 任意（例: `XSkillProject`）
   - Use case: **「Making a bot」**
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

```bash
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
pip install -r requirements.txt

# 確認のみ（投稿しない）
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
| `503 Service Unavailable` | Freeプラン廃止・クレジット未登録 | Step 1のPay Per Use登録を完了する |
| `403 Forbidden` | App Permissionsが「Read」のまま | Step 3→4をやり直す |
| `401 Unauthorized` | APIキーが間違っている | .envを確認・コピーミスがないか |
| `401 Unauthorized` | API KeyとAccess Tokenが不一致 | Access TokenをRegenerateし直す |
| `429 Too Many Requests` | レート制限超過 | しばらく待つ（自動リトライあり） |

---

## 料金（Pay Per Use）

| 操作 | 単価 | 月100回の場合 |
|------|------|------------|
| ツイート投稿（write） | $0.01/件 | **$1/月** |
| 初回参加ボーナス | **$500クレジット** | 約40年分相当 |

> 月額固定費なし。使った分だけ課金。
