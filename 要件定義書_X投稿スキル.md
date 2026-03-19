# X投稿スキル 要件定義書

**作成日**: 2026-03-19
**リポジトリ**: https://github.com/dejiinaworks-png/X-skill
**ステータス**: 初版（リサーチ結果に基づく提案）

---

## 0. エグゼクティブサマリー

本スキルは「noteで記事を書く日本人クリエイター・個人事業主」向けに、
**note記事 → AI変換 → X自動投稿** を一気通貫で行うClaude Codeスキルです。

### 発見した最大の差別化ポイント（空白地帯）
> 「note.com専用 × 日本語AI変換 × X自動投稿スキル」は国内外に**競合ゼロ**

| 既存ツールの問題 | 本スキルの解決策 |
|----------------|----------------|
| Buffer/Hootsuite: 日本語対応が弱い | Claude APIによる自然な日本語生成 |
| SocialDog: AI投稿生成が限定的 | note記事の構造を理解した深い変換 |
| 汎用ツール: note連携がない | note非公式APIでダイレクト取得 |
| 海外ツール: 月$29〜高い | X API Free枠＋Claudeで低コスト運用 |

---

## 1. プロジェクト概要

### 1.1 目的

- **主目的**: noteの記事をXに最適化した投稿文へ自動変換・投稿する
- **副目的**: Claude Codeスキルとして公開し、同様の悩みを持つユーザーに配布する

### 1.2 ターゲットユーザー

| 属性 | 詳細 |
|------|------|
| noteクリエイター | 月1〜10記事を書く個人ブロガー・フリーランス |
| X運用したいが手間がかかる人 | 記事を書いたらXにも流したいが変換が面倒 |
| 技術レベル | 「Claudeに話しかけるだけ」で完結させたい非エンジニア |
| 課金感度 | 月1,000〜3,000円なら許容できる層 |

### 1.3 解決する問題

1. note記事を書いた後、Xへの転用に時間がかかる
2. そのまま貼り付けても反応が取れない（長すぎ・フォーマット違い）
3. 毎回手動で投稿するのが続かない
4. 何時に何を投稿すればいいかわからない

---

## 2. システム全体構成

```
┌─────────────────────────────────────────────────────────┐
│                   ユーザー（Claude Code）                  │
│  「このnote記事からX投稿を作って」                          │
└──────────────────────┬──────────────────────────────────┘
                       │ /x-post または /note-to-x
                       ▼
┌─────────────────────────────────────────────────────────┐
│              X投稿スキル（SKILL.md）                       │
│                                                          │
│  ① note記事取得     ② AI文章変換     ③ X投稿              │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐         │
│  │note非公式 │ →  │Claude API │ →  │X API v2  │         │
│  │API / RSS  │     │プロンプト │     │Tweepy    │         │
│  └──────────┘     └──────────┘     └──────────┘         │
│                                                          │
│  ④ スケジューラー  ⑤ 品質チェック  ⑥ 分析               │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐         │
│  │cron / GH  │     │文字数・   │     │投稿実績  │         │
│  │Actions    │     │フック強度 │     │ログ管理  │         │
│  └──────────┘     └──────────┘     └──────────┘         │
└─────────────────────────────────────────────────────────┘
```

---

## 3. フォルダ構成（公開スキルとして）

```
X-skill/                                    ← GitHubリポジトリroot
│
├── README.md                               ← インストール手順・使い方
├── CHANGELOG.md                            ← バージョン履歴
├── LICENSE                                 ← MIT
├── .gitignore                              ← .env除外必須
├── .env.example                            ← 必要な環境変数テンプレート
│
├── .claude-plugin/
│   └── plugin.json                         ← プラグインメタデータ
│
├── skills/
│   ├── note-to-x/                          ← メインスキル
│   │   ├── SKILL.md                        ← /note-to-x コマンド定義
│   │   ├── references/
│   │   │   ├── note-api.md                 ← note非公式APIエンドポイント集
│   │   │   ├── x-post-formats.md           ← 高エンゲージ投稿フォーマット集
│   │   │   └── prompt-templates.md         ← Claude API プロンプトテンプレート
│   │   └── scripts/
│   │       ├── fetch_note.py               ← note記事取得
│   │       ├── generate_posts.py           ← AI投稿文生成
│   │       └── post_to_x.py               ← X投稿実行
│   │
│   ├── x-scheduler/                        ← スケジュール管理スキル
│   │   ├── SKILL.md                        ← /x-scheduler コマンド定義
│   │   └── scripts/
│   │       ├── schedule.py                 ← 投稿スケジュール管理
│   │       └── queue.json                  ← 投稿キュー
│   │
│   └── x-analytics/                        ← 分析スキル（Phase4以降）
│       ├── SKILL.md
│       └── scripts/
│           └── analyze.py
│
├── .claude/
│   ├── commands/                           ← シンプルコマンド
│   │   └── x-setup.md                     ← /x-setup（初期設定ガイド）
│   └── settings.json
│
├── .mcp.json                               ← MCPサーバー設定
│
├── docs/
│   ├── SETUP.md                            ← X API開通手順詳細
│   ├── NOTE_API.md                         ← note API利用ガイド
│   └── POST_STRATEGY.md                   ← 投稿戦略ガイド
│
└── .github/
    └── workflows/
        ├── release.yml                     ← 自動リリース
        └── x-scheduler.yml                ← GitHub Actions定期投稿
```

---

## 4. Phase別実装計画

### Phase 0: X API開通（最初に実施）

**目的**: 実際にXへ投稿できる環境を整える

#### 手順（詳細）

```
Step 1: X Developer Portal でアカウント登録
  → https://developer.x.com にアクセス
  → 「Sign up for Free Account」
  → 利用目的を250文字以上で記述（英語推奨）

Step 2: プロジェクト・アプリ作成
  → ダッシュボードで「+ Create Project」
  → 「+ Create App」
  → API Key & Secret, Bearer Token を保存（1度しか表示されない）

Step 3: OAuth 1.0a 権限設定（重要）
  → Settings > User authentication settings
  → App permissions: 「Read and Write」を選択（デフォルトはRead only）
  → Type of App: 「Web App, Automated App or Bot」
  → Callback URI: http://localhost:8080/callback

Step 4: Access Token 再生成（必須）
  → Keys and Tokens > Access Token and Secret > Regenerate
  ※ 権限変更後は必ず再生成。古いトークンはRead-onlyのまま

Step 5: .env ファイルに5つのキーを設定
  API_KEY=
  API_KEY_SECRET=
  BEARER_TOKEN=
  ACCESS_TOKEN=
  ACCESS_TOKEN_SECRET=
```

#### Tier選択指針

| 投稿量 | 推奨Tier | 月額 |
|--------|---------|------|
| 月500件以内（個人テスト） | **Free** | $0 |
| 月500〜5,000件（本番運用） | Basic | $200 |
| 月500件以内＋低コスト重視 | **TwitterAPI.io** | ~$0.075 |

**最初はFree Tier（$0）から開始を推奨**

#### 最小実装コード

```python
# requirements.txt
tweepy>=4.14.0
python-dotenv>=1.0.0
feedparser>=6.0.0
anthropic>=0.40.0
requests>=2.31.0

# post_to_x.py（テスト投稿）
import tweepy, os
from dotenv import load_dotenv
load_dotenv()

client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_KEY_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
)
response = client.create_tweet(text="X-skill テスト投稿 ✅")
print(f"投稿成功: {response.data['id']}")
```

---

### Phase 1: note記事取得

**目的**: note.comから記事を自動取得する

#### 実装方針（優先順位順）

| 方法 | 安定性 | コスト | 推奨度 |
|------|--------|--------|--------|
| **RSS フィード** | 高（公式提供） | 無料 | ◎ |
| **非公式API** | 中（変更リスク） | 無料 | ○ |
| Playwright スクレイピング | 中 | 無料 | △ |

#### 非公式APIエンドポイント（2026年3月確認済み）

```python
BASE = "https://note.com/api"

# ユーザーの記事一覧
GET {BASE}/v2/creators/{username}/contents?kind=note&page=1

# キーワード検索
GET {BASE}/v3/searches?context=note&q={keyword}&size=20&start=0

# 記事詳細（本文HTML含む）
GET {BASE}/v3/notes/{note_id}

# RSSフィード（最安定）
https://note.com/{username}/rss
```

#### fetch_note.py の設計

```python
# 入力: noteのURL or ユーザー名 or キーワード
# 出力: {title, body, url, published_at, headings[]}
# レート制限: リクエスト間5秒以上のディレイ必須
```

---

### Phase 2: AI文章変換（核心機能）

**目的**: note記事をXで反応が取れる投稿文に変換する

#### 変換フロー

```
note記事
  │
  ├─→ [A] フック単体投稿（1本）   ← noteタイトルを変形
  ├─→ [B] 知識ポスト（2〜4本）   ← 見出しH2を1つずつ切り出し
  ├─→ [C] 共感エピソード（1本）  ← 本文のストーリー部分を抽出
  ├─→ [D] スレッド形式（5〜7本） ← 記事全体を展開
  └─→ [E] note誘導ポスト（1本）  ← URL付き（最後に投稿）
```

#### 高エンゲージメント投稿フォーマット

**フォーマットA: 問題提起型（最頻出バズ型）**
```
○○している人、
実は○○○できていません。

理由は○○○だから。

具体的には、
・ポイント1
・ポイント2
・ポイント3

→ 「○○派？○○派？」
```

**フォーマットB: 衝撃事実列挙型**
```
○年間○○をやり続けて気づいた○個のこと

①〜〜〜
②〜〜〜
③〜〜〜

あなたはいくつ知ってた？
```

**フォーマットC: 共感エピソード型**
```
○○していたら、○○に言われた。
「○○○○○」

最初は○○だったけど、
今は○○だと思っている。

あなたはどう思いますか？
```

#### 投稿品質ルール

| ルール | 内容 |
|--------|------|
| 文字数 | 80〜140文字（日本語） |
| 改行 | 15〜20文字ごと |
| 絵文字 | 1投稿2〜4個・行頭か行末のみ |
| URL | 本文に含めない（アルゴリズムペナルティ回避） |
| ハッシュタグ | 0〜2個（多すぎはスパム判定） |
| CTA | 末尾に必ず入れる（リプライ誘発型） |

#### Claude API プロンプト（基本形）

```
# 役割
あなたはX（Twitter）でエンゲージメントを最大化する
SNSマーケティング専門家です。

# タスク
以下のnote記事から、X投稿を3パターン生成してください。

## note記事
{title}
{body}

# 制約
- 文字数：140文字以内（日本語）
- フック：1行目でスクロールを止める
- 改行：15〜20文字ごと
- URL・ハッシュタグなし
- CTAを末尾に入れる
- AIっぽい表現を避ける

# 出力形式
【パターンA：問題提起型】
【パターンB：共感型】
【パターンC：数字・データ型】
```

---

### Phase 3: X自動投稿

**目的**: 生成した投稿文をXに実際に投稿する

#### 機能要件

- [ ] テキスト投稿（単体）
- [ ] 画像付き投稿（OAuth 1.0a 必須）
- [ ] スレッド投稿（連続ツイート）
- [ ] レート制限ハンドリング（指数バックオフ）
- [ ] 投稿ログ保存（JSON）

#### エラー対応表

| エラーコード | 原因 | 対処法 |
|------------|------|--------|
| 403 Forbidden | App Permissionsが「Read」のまま | Write権限に変更→トークン再生成 |
| 429 Too Many Requests | レート制限超過 | 指数バックオフ（60s→120s→240s） |
| 401 Unauthorized | トークン不正 | 環境変数を確認・再生成 |
| 402 CreditsDepleted | 課金不足（新規アカウント） | $5以上のクレジット購入 |

---

### Phase 4: スケジューラー

**目的**: 最適な時間に自動投稿する

#### 最適投稿時間帯（日本・2026年版）

```
最優先: 水曜日 9:00
次点:   火・木  8:00〜10:00
        月〜金  12:00〜13:00（ランチタイム）
        月〜木  20:00〜22:00（夜間）
避けるべき: 0〜6時、土日の昼間
```

#### 実装方法（選択肢）

| 方法 | コスト | 難易度 | 推奨度 |
|------|--------|--------|--------|
| **GitHub Actions cron** | 無料 | 低 | ◎ |
| Google Apps Script | 無料 | 低 | ○ |
| ローカル cron（常時起動PC） | 無料 | 低 | △ |

#### GitHub Actions設定例

```yaml
# .github/workflows/x-scheduler.yml
name: X Auto Post
on:
  schedule:
    - cron: '0 0 * * 3'   # 毎週水曜9時(JST=UTC+9 → UTC 0時)
    - cron: '0 3 * * 2,4' # 火・木 12時(JST)
jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python skills/note-to-x/scripts/post_to_x.py
    env:
      API_KEY: ${{ secrets.API_KEY }}
      ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN }}
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

---

### Phase 5: 分析・改善（将来）

- 投稿別インプレッション・エンゲージメント追跡
- 高パフォーマンス投稿パターンの自動学習
- A/Bテスト（複数パターン生成→最良選択）

---

## 5. SKILL.md 設計（公開スキルの核心）

### /note-to-x スキル

```yaml
---
name: note-to-x
description: |
  note.comの記事をX（Twitter）向けの高エンゲージメント投稿文に変換し、
  自動投稿またはドラフト保存する。
  「noteをXに投稿したい」「note記事をツイートに変換」と言われたら使用。
argument-hint: "[note URL または キーワード] [--draft|--post|--schedule]"
allowed-tools: Bash(python *), Read, Write
---

## 実行フロー

1. note記事を取得: `python ${CLAUDE_SKILL_DIR}/scripts/fetch_note.py "$0"`
2. 投稿文を生成: `python ${CLAUDE_SKILL_DIR}/scripts/generate_posts.py`
3. ユーザーに3パターン提示して確認を取る
4. 承認後に投稿: `python ${CLAUDE_SKILL_DIR}/scripts/post_to_x.py`

## オプション
- `--draft`: 投稿せずにドラフト保存のみ
- `--post`: 確認なしで即投稿
- `--schedule`: スケジュールキューに追加

詳細フォーマット仕様は references/x-post-formats.md を参照。
```

---

## 6. 使用するMCP・ライブラリ

### 推奨MCP構成

| 用途 | 推奨ツール | 理由 |
|------|-----------|------|
| X投稿実行 | **Composio Twitter MCP** | OAuth管理不要・SOC2準拠・Claude Code対応 |
| X投稿（代替） | rafaljanicki/x-twitter-mcp-server | 1コマンドインストール・v2完全実装 |
| コンテンツリサーチ | **Xpoz MCP** | APIキー不要・15億件DB・インストール不要 |
| 投稿文生成 | X Writing Assistant Skill (mcpmarket) | AIっぽさ排除済み・高品質 |

### .mcp.json 設計

```json
{
  "mcpServers": {
    "twitter": {
      "command": "composio-mcp",
      "args": ["--toolkit", "twitter"],
      "env": {
        "COMPOSIO_API_KEY": "${COMPOSIO_API_KEY}"
      }
    },
    "xpoz": {
      "url": "https://mcp.xpoz.ai/sse",
      "type": "sse"
    }
  }
}
```

### Pythonライブラリ（requirements.txt）

```
tweepy>=4.14.0          # X API v2 公式ラッパー
anthropic>=0.40.0       # Claude API
python-dotenv>=1.0.0    # 環境変数管理
feedparser>=6.0.0       # note RSS取得
requests>=2.31.0        # note 非公式API
schedule>=1.2.0         # ローカルスケジューラー
```

---

## 7. 環境変数一覧（.env.example）

```bash
# === X API（必須） ===
API_KEY=                      # X Developer Portal > Keys and Tokens
API_KEY_SECRET=
BEARER_TOKEN=
ACCESS_TOKEN=
ACCESS_TOKEN_SECRET=

# === Claude API（必須） ===
ANTHROPIC_API_KEY=            # https://console.anthropic.com

# === note.com（任意） ===
NOTE_USERNAME=                # 取得対象のnoteユーザー名
NOTE_SESSION_TOKEN=           # 有料記事取得時のみ（通常不要）

# === オプション ===
POST_LANGUAGE=ja              # 投稿言語（ja/en）
POST_TONE=casual              # 文体（casual/formal/expert）
MAX_POSTS_PER_DAY=5           # 1日の最大投稿数
MIN_INTERVAL_MINUTES=60       # 投稿間隔（分）
OUTPUT_DIR=./output           # 投稿ログ保存先
```

---

## 8. セキュリティ要件

### 必須対応

- [ ] `.env` を `.gitignore` に追加（絶対漏洩させない）
- [ ] `API_KEY` 等をコードにハードコードしない
- [ ] GitHub Secrets に本番キーを登録（Actions用）
- [ ] 投稿ログにトークン値を出力しない

### X APIポリシー準拠

- [ ] 投稿間隔: 最低60秒以上空ける
- [ ] 同一内容の連続投稿禁止（スパム判定）
- [ ] 自動いいね・自動フォローは実装しない
- [ ] 1日5〜10投稿を上限とする（シャドウバン防止）

---

## 9. コスト試算

### 月間コスト（個人利用・月100投稿想定）

| サービス | 月額 |
|---------|------|
| X API Free Tier | **$0** |
| Claude API（claude-sonnet-4-6 × 100回） | ~$1〜2 |
| GitHub Actions（無料枠内） | **$0** |
| **合計** | **~$1〜2/月** |

### 月間コスト（本格運用・月500〜1000投稿想定）

| サービス | 月額 |
|---------|------|
| X API Free Tier（500件まで） | **$0** |
| TwitterAPI.io（超過分） | ~$0.15/1,000件 |
| Claude API | ~$5〜10 |
| **合計** | **~$5〜10/月** |

---

## 10. 実装優先順位（ロードマップ）

```
Week 1（今すぐ開始）
  ├── [P0] X API 開通（Developer Portal登録〜テスト投稿）
  ├── [P0] フォルダ構成の作成（公開スキルの骨格）
  └── [P0] .env.example と .gitignore の整備

Week 2
  ├── [P1] note RSS/API 記事取得スクリプト
  ├── [P1] Claude API 投稿文生成（3パターン出力）
  └── [P1] SKILL.md の初版（/note-to-x コマンド）

Week 3
  ├── [P2] X投稿スクリプト（エラーハンドリング付き）
  ├── [P2] 人間レビューフロー（承認後投稿）
  └── [P2] 投稿ログ保存

Week 4
  ├── [P3] GitHub Actions スケジューラー
  ├── [P3] README.md（公開用）完成
  └── [P3] v1.0.0 リリース → GitHub・各マーケットプレイスに公開
```

---

## 11. 公開先マーケットプレイス（v1.0リリース後）

| マーケット | URL | 形式 |
|-----------|-----|------|
| SkillsMP | https://skillsmp.com/ | SKILL.md |
| MCPmarket | https://mcpmarket.com/ | スキル形式 |
| Smithery | https://smithery.ai/ | プラグイン形式 |
| GitHub Marketplace | Actions/Workflows | GitHub Actions |

---

## 12. 今後の拡張アイデア

| アイデア | 優先度 | 詳細 |
|---------|--------|------|
| Bluesky同時投稿 | 中 | Social MCP（kitadmin01）で対応可能 |
| Instagram/Threads | 低 | Social Media MCP Server で対応可能 |
| YouTube文字起こし→X変換 | 中 | YouTube transcript API + 同フロー |
| 文体スライダー | 高 | 断言調/丁寧語/口語を選択可能に |
| A/Bテスト機能 | 中 | 複数パターンを時間差で投稿して比較 |
| Xアナリティクス連携 | 低 | Xpoz MCPで実装可能 |

---

## 参考リソース

- [X Developer Portal](https://developer.x.com)
- [X API Rate Limits](https://docs.x.com/x-api/fundamentals/rate-limits)
- [Tweepy ドキュメント](https://www.tweepy.org/)
- [Claude Code Skills 公式ドキュメント](https://code.claude.com/docs/en/skills)
- [Composio Twitter MCP](https://composio.dev/toolkits/twitter/framework/claude-code)
- [note 非公式API一覧（2025）](https://note.com/masuyohasiri/n/n1e8161d81866)
- [Postiz OSS（参考実装）](https://github.com/gitroomhq/postiz-app)

---

*このドキュメントは7エージェントによる並列リサーチ（X API・投稿法則・MCP市場・APIコスト・Reddit・キーワード・フォルダ構成）の結果を統合して作成しました。*
