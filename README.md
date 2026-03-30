# X投稿くん (X-skill)

X（旧Twitter）・Threads への自動投稿・スケジュール管理ツール。

**バージョン: 2.0.0**

---

## 概要

- note記事URLを渡すと、ナレッジに基づいてX投稿文を自動生成
- Google スプレッドシートに予約投稿データを書き込み
- GAS（Google Apps Script）が自動でX / Threads に投稿
- Klavis MCP 経由でスプレッドシートをClaudeから直接操作可能

---

## アーキテクチャ

### v2.0（現行）: GAS + スプレッドシート + Claude

```
[Claude（X投稿くん）]
  ↓ note記事URL を受け取る
  ↓ ナレッジに基づいて投稿文を生成
  ↓ Klavis MCP でスプレッドシートに書き込み
        ↓
[Googleスプレッドシート]（投稿データ管理）
        ↓
[Google Apps Script]（30分ごとに自動実行）
        ↓
[X API v2 / Threads API]（自動投稿）
```

**メリット:**
- git push 不要・状態管理がシートのセルで完結
- Google インフラのため cron 遅延なし
- スプレッドシートで投稿内容を直接確認・編集可能
- Claude から Klavis MCP 経由でシートを操作可能

### v1（GitHub Actions）

```
queue/queue.json → GitHub Actions（cron） → X API v2
```

現在はバックアップとして残存。`.github/workflows/auto-post.yml` 参照。

---

## クイックスタート

### 1. スプレッドシートを新規作成する

1. [Googleスプレッドシート](https://sheets.google.com) で新規シートを作成
2. シート名を `X投稿` に変更
3. `skills/gas-x-post/SETUP.md` の手順に従ってGASを設定
4. 作成したスプレッドシートのIDをGASのスクリプトプロパティに設定

> スプレッドシートのIDはURLの `https://docs.google.com/spreadsheets/d/【ここ】/edit` の部分です。

### 2. Claude に依頼するだけ

```
「この記事をもとにX投稿を3本作成して、明日のスケジュールで登録してください」
https://note.com/あなたのnoteユーザー名/n/記事ID
```

Claude が自動で:
1. 記事を取得
2. ナレッジ（`skills/x-post-writer/SKILL.md`）に従って投稿文生成
3. スプレッドシートの空き行に書き込み
4. GASが自動投稿

---

## GAS セットアップ手順（初回のみ）

詳細: `skills/gas-x-post/SETUP.md`

### 必要なもの

- Google アカウント
- X Developer App（API キー4つ）
- Threads API アクセストークン（Threads 投稿する場合）

### APIキーの設定場所

**GASエディタ**の「プロジェクトの設定」→「スクリプトプロパティ」に設定する。
コードには書かない。GitHubには絶対にアップロードしない。

| プロパティ名 | 内容 |
|---|---|
| X_API_KEY | X の API キー |
| X_API_SECRET | X の API シークレット |
| X_ACCESS_TOKEN | X のアクセストークン |
| X_ACCESS_TOKEN_SECRET | X のアクセストークンシークレット |
| THREADS_ACCESS_TOKEN | Threads のアクセストークン |
| THREADS_USER_ID | 空欄でOK（初回実行時に自動取得） |

### セットアップ手順

1. スプレッドシートを開く
2. 「拡張機能」→「Apps Script」
3. `skills/gas-x-post/Code.gs` の内容を全て貼り付けて保存
4. スクリプトプロパティにAPIキーを設定
5. `setupTrigger` を実行 → 30分ごとの自動実行が開始

---

## スプレッドシート列構成

| 列 | 内容 | 備考 |
|---|---|---|
| A | 投稿日 | 例: 2026/3/25 |
| B | 時 | 0〜23 |
| C | 分 | 0〜59 |
| D | 投稿内容 | テキスト本文 |
| E | X投稿する | TRUE/FALSE |
| F | Threads投稿する | TRUE/FALSE |
| G〜J | 画像1〜4 URL | 任意 |
| K | 投稿済み | GASが自動更新 |
| L | X投稿URL | GASが自動記入 |
| M | Threads投稿URL | GASが自動記入 |

---

## 投稿コンテンツ作成ワークフロー

`skills/x-post-writer/SKILL.md` に完全なワークフローを定義。

### 6ステップ

1. **記事取得** - WebFetch で本文・タイトル・キーワードを取得
2. **インサイト分析** - ターゲットの本音・潜在的欲求を掘り下げる
3. **フック選択** - 50パターンから毎回異なるパターンを選択
4. **投稿文生成** - 文体DNA・100点法則に従って生成
5. **AI臭除去チェック** - 20項目チェックリストを通過
6. **スプレッドシート書き込み** - Klavis MCP 経由で自動書き込み

### ナレッジ一覧

| ファイル | 内容 |
|---|---|
| `00_インサイト分析手法.md` | ターゲットの本音を暴く手法 |
| `01_文体DNA.md` | 人間らしい文体の再現方法 |
| `02_フック50パターン.md` | 冒頭フック50パターン集 |
| `03_長文構造.md` | 3000字投稿の14ブロック構造 |
| `04_AI臭除去.md` | AI臭をなくすルール・NGワード集 |
| `05_対比パターン完全ガイド.md` | 対比型投稿の作り方 |
| `06_既視感ゼロ戦略.md` | 独自の切り口の作り方 |
| `07_繰り返し回避ルール.md` | 同じ表現を使わないルール |
| `08_100点ポストの絶対法則.md` | 高品質投稿の8法則 |
| `09_ポストデザイン理論.md` | 視覚的なポスト設計 |
| `10_フローチャート単独型パターン.md` | フロー形式の投稿パターン |
| `11_箇条書き単独型パターン.md` | 箇条書き形式の投稿パターン |

---

## ファイル構成

```
X投稿くん/
├── skills/
│   ├── x-post-writer/          # 投稿文生成スキル（メイン）
│   │   ├── SKILL.md            # ワークフロー定義・運用ルール
│   │   └── knowledge/          # 投稿品質向上ナレッジ（12ファイル）
│   ├── gas-x-post/             # GAS自動投稿スクリプト（v2.0 現行）
│   │   ├── Code.gs             # GASスクリプト本体
│   │   └── SETUP.md            # セットアップ詳細手順
│   ├── note-to-x/              # note記事→X投稿変換（補助）
│   └── ナレッジ/               # 旧ナレッジ格納場所（x-post-writerに移行済み）
├── queue/                      # v1用キューデータ
│   ├── queue.json
│   └── posted_ids.json
├── docs/                       # ドキュメント類
├── .github/
│   └── workflows/
│       └── auto-post.yml       # v1 GitHub Actions（バックアップ）
├── .gitignore
└── README.md
```

---

## Mac / 別PCへの引き継ぎ方法

GitHub からクローンするだけで環境を引き継げます。

```bash
git clone https://github.com/dejiinaworks-png/X-skill.git
cd X-skill
```

**ただし、以下は GitHub に保存されていないため別途設定が必要:**

| 項目 | 保存場所 | 引き継ぎ方法 |
|------|---------|------------|
| X APIキー | GASスクリプトプロパティ | スプレッドシートはGoogle上にあるので自動引き継ぎ |
| Threads APIキー | GASスクリプトプロパティ | 同上 |
| Klavis MCP設定 | Claude Code（`claude mcp list`） | Macの Claude Code で `claude mcp add` を再実行 |

**GASとスプレッドシートはGoogle上にあるので、スプレッドシートのURLさえ分かれば引き継ぎ済みです。**

---

## 開発ログ

変更履歴は [Issues](https://github.com/dejiinaworks-png/X-skill/issues) を参照。

---

## ライセンス

Copyright (c) 2025 株式会社デジイナ

使用・改変・商用利用（社内利用の範囲内）は自由です。
ただし、ソースコードおよびその改変版の再配布は禁止します。
詳細は [LICENSE](./LICENSE) を参照してください。
