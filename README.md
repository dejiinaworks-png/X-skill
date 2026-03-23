# X投稿くん (X-skill)

X（旧Twitter）・Threads への自動投稿・スケジュール管理ツール。

**バージョン: 2.0.0**

---

## 概要

- X / Threads へのスケジュール投稿を自動化
- Google スプレッドシート + GAS による管理（v2.0〜）
- X投稿ナレッジに基づいたコンテンツ生成サポート
- GitHub Actions による投稿（v1系、現在はバックアップ用途）

---

## アーキテクチャ

### v2.0（現行）: GAS + スプレッドシート

```
スプレッドシート（投稿データ管理）
        ↓
Google Apps Script（30分ごとに自動実行）
        ↓
X API v2 / Threads API
```

**メリット:**
- git push 不要・状態管理がシートのセルで完結
- Google インフラのため cron 遅延なし
- スプレッドシートで投稿内容を直接編集可能

### v1（GitHub Actions）

```
queue/queue.json → GitHub Actions（cron） → X API v2
```

現在はバックアップとして残存。`.github/workflows/auto-post.yml` 参照。

---

## GAS セットアップ手順

### 必要なもの

- Google アカウント
- X Developer App（API キー4つ）
- Threads API アクセストークン（Threads投稿する場合）

### スプレッドシート

本番スプレッドシート: `skills/gas-x-post/` 配下のスクリプトで管理

#### 列構成

| 列 | 内容 | 備考 |
|---|---|---|
| A | 投稿日 | 例: 2026/3/23 |
| B | 時 | 0〜23 |
| C | 分 | 0〜59 |
| D | 投稿内容 | テキスト本文 |
| E | X投稿する | チェックボックス |
| F | Threads投稿する | チェックボックス |
| G〜J | 画像1〜4 URL | 任意 |
| K | 投稿済み | 自動記入 |
| L | X投稿URL | 自動記入 |
| M | Threads投稿URL | 自動記入 |

### 手順

**Step 1: GASにコードを貼り付け**

1. スプレッドシートを開く（新規 or 既存どちらでも可）
2. 「拡張機能」→「Apps Script」
3. エディタの内容を全て削除
4. `skills/gas-x-post/Code.gs` の内容を貼り付けて保存（Ctrl+S）

**Step 2: スクリプトプロパティにAPIキーを設定**

GASエディタの「⚙️ プロジェクトの設定」→「スクリプトプロパティ」で以下を追加：

| プロパティ名 | 内容 |
|---|---|
| X_API_KEY | X の API キー |
| X_API_SECRET | X の API シークレット |
| X_ACCESS_TOKEN | X のアクセストークン |
| X_ACCESS_TOKEN_SECRET | X のアクセストークンシークレット |
| THREADS_ACCESS_TOKEN | Threads のアクセストークン |
| THREADS_USER_ID | 空欄でOK（初回実行時に自動取得） |

**Step 3: `setupSpreadsheet` を実行**

関数ドロップダウンで `setupSpreadsheet` を選択 → ▶ 実行

- `X投稿` シートが自動作成される
- ヘッダー・チェックボックス・初期データが自動投入される
- 初回実行時は権限の承認ダイアログが出るので「許可」をクリック

**Step 4: `dryRun` で動作確認**

関数ドロップダウンで `dryRun` を選択 → ▶ 実行

次の投稿対象がログに表示されれば正常。

**Step 5: `setupTrigger` を実行**

関数ドロップダウンで `setupTrigger` を選択 → ▶ 実行

30分ごとの自動実行トリガーが登録される。以後は何もしなくてOK。

### 重複投稿防止の仕組み

```
実行 → K列(投稿済み) が TRUE → スキップ
     → L列(X URL) が入力済み → X 再投稿しない
     → M列(Threads URL) が入力済み → Threads 再投稿しない
```

---

## 投稿コンテンツ作成ガイドライン

`skills/ナレッジ/X投稿ナレッジ/` 配下のナレッジを参照。

| ファイル | 内容 |
|---|---|
| 00_インサイト分析手法.md | ターゲットの本音を暴く手法 |
| 01_文体DNA.md | 人間らしい文体の再現方法 |
| 02_フック50パターン.md | 冒頭フックのパターン集 |
| 04_AI臭除去.md | AI臭をなくすルール |
| 08_100点ポストの絶対法則.md | 高品質投稿の評価基準 |
| 09_ポストデザイン理論.md | 視覚的なポスト設計 |

---

## ファイル構成

```
X投稿くん/
├── skills/
│   ├── gas-x-post/          # GAS自動投稿スクリプト（v2.0 現行）
│   │   ├── Code.gs          # GASスクリプト本体
│   │   └── SETUP.md         # セットアップ詳細手順
│   ├── note-to-x/           # note記事→X投稿変換スクリプト
│   │   └── scripts/
│   │       └── dequeue_post.py
│   └── ナレッジ/
│       └── X投稿ナレッジ/   # 投稿品質向上ナレッジ
├── queue/                   # v1用キューデータ
│   ├── queue.json
│   └── posted_ids.json
├── .github/
│   └── workflows/
│       └── auto-post.yml    # v1 GitHub Actions（バックアップ）
└── README.md
```

---

## 開発ログ

変更履歴は [Issues](https://github.com/dejiinaworks-png/X-skill/issues) を参照。
