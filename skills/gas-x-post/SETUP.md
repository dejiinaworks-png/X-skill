# GAS X自動投稿 セットアップ手順

## スプレッドシート列構成

| 列 | ヘッダー名 | 内容 | 備考 |
|---|---|---|---|
| A | 投稿日 | 2026/3/23 | 日付形式 |
| B | 時 | 7 | 数値（0〜23） |
| C | 分 | 0 | 数値（0〜59） |
| D | 投稿内容 | テキスト本文 | |
| E | X投稿する | TRUE/FALSE | チェックボックス |
| F | Threads投稿する | TRUE/FALSE | チェックボックス |
| G | 画像1 URL | https://... | 任意 |
| H | 画像2 URL | https://... | 任意 |
| I | 画像3 URL | https://... | 任意 |
| J | 画像4 URL | https://... | 任意 |
| K | 投稿済み | TRUE/FALSE | 自動記入・チェックボックス |
| L | X投稿URL | https://x.com/... | 自動記入 |
| M | Threads投稿URL | https://threads.net/... | 自動記入 |

---

## 初期データ（Antigravity vs ClaudeCode 5件）

シート名: `X投稿` の2行目以降に貼り付け

```
投稿日	時	分	投稿内容	X投稿する	Threads投稿する	画像1	画像2	画像3	画像4	投稿済み	X投稿URL	Threads投稿URL
2026/3/23	7	0	「AntigravityってClaude Codeに勝てるの？」とか言いながら、実は乗り遅れるのが怖いだけの人へ。

Googleが完全無料でぶっ込んできたAI IDE、1週間本気で使い込んだ。

結論：今すぐ乗り換えじゃないけど、無視できない理由がある。

詳細↓
https://note.com/ina_tatsu44/n/nb88d80f03bb8

#AI開発 #ClaudeCode #Antigravity	TRUE	FALSE
2026/3/23	12	0	Antigravityを触って「あ、Googleが本気だな」と思った瞬間。

AIエージェントを複数並列実行できる
→ Claude Codeは基本1タスク順番待ち

ブラウザテストが最初から内蔵
→ Playwrightを自前設定してた俺、何してたんだろうw

完全無料（プレビュー中）
→ いつ課金に切り替わるか不明。今のうちに触っとく価値はある。

https://note.com/ina_tatsu44/n/nb88d80f03bb8

#Antigravity #AI開発ツール	TRUE	FALSE
2026/3/23	19	0	Claude Codeが向いてる案件
→ 既存の大規模コード改修、本番環境・安全性重視、チーム開発・MCP連携

Antigravityが向いてる案件
→ フロントエンドの新規開発、ブラウザ動作を繰り返し確認する作業、「とにかく今すぐ無料で試したい」

どちらが上じゃない。用途次第。

https://note.com/ina_tatsu44/n/nb88d80f03bb8

#AIツール #エンジニア	TRUE	FALSE
2026/3/23	21	0	正直に言う。

今の業務ならClaude Code一択。コードベース全体を200kトークンで把握する力は、大きいリポジトリで特に差が出る。

ただ。

Antigravityはフロントエンドとブラウザテスト文脈で急成長してる。Googleのインフラ力は正直脅威。

半年後に「あのとき触っとけばよかった」はなりたくない。今のうちに両方知っておく価値はある。

https://note.com/ina_tatsu44/n/nb88d80f03bb8

#ClaudeCode #Antigravity	TRUE	FALSE
2026/3/24	7	0	Claude Code vs Antigravity、整理した。

Claude Code
→ $20/月〜 / 200kトークンでコードベース全理解 / 本番・チーム・MCP連携向き

Antigravity
→ 完全無料（プレビュー中）/ 自律エージェント並列実行 / フロントエンド・自動化向き

どちらが上じゃない。「何を作るか」で使い分けるだけ。

https://note.com/ina_tatsu44/n/nb88d80f03bb8

#AI #開発効率化 #プログラミング	TRUE	FALSE
```

---

## セットアップ手順

### 1. スプレッドシートを準備

1. 既存スプレッドシートに `X投稿` シートを作成（または既存シートの名前を変更）
2. 1行目にヘッダーを入力
3. E列・F列・K列をチェックボックス形式に設定（書式 → チェックボックス）
4. 上記データを2行目以降に貼り付け

### 2. GASスクリプトを設定

1. スプレッドシートから「拡張機能」→「Apps Script」を開く
2. `Code.gs` の内容を全て貼り付けて保存（Ctrl+S）
3. ※既存のスクリプトを完全に置き換える

### 3. スクリプトプロパティを更新

「プロジェクトの設定」→「スクリプトプロパティ」で以下を設定：

| プロパティ名 | 値 |
|---|---|
| X_API_KEY | （新しい値） |
| X_API_SECRET | （新しい値） |
| X_ACCESS_TOKEN | （新しい値） |
| X_ACCESS_TOKEN_SECRET | （新しい値） |
| THREADS_ACCESS_TOKEN | （新しい値）※Threads投稿しない場合は不要 |
| THREADS_USER_ID | （自動取得されるので空欄でOK） |

### 4. トリガーを設定

GASエディタで `setupTrigger` 関数を実行（▶ボタン）
→ 30分ごとに `postNextScheduledItem` が自動実行されます

### 5. 動作確認

`dryRun` 関数を実行して次の投稿対象が正しく表示されるか確認

---

## 重複投稿防止の仕組み

```
実行 → K列(投稿済み)がTRUE → スキップ
       L列(X URL)が入力済み → X再投稿しない
       M列(Threads URL)が入力済み → Threads再投稿しない
```

- 投稿成功: URLをL/M列に書き込み → K列をTRUEに更新
- 投稿失敗: エラーメッセージをL/M列に書き込み（次回リトライ可能）
- git pushの問題が**構造的に発生しない**（Googleのインフラ上で完結）
