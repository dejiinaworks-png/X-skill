"""
NanoBanana2 スライドプロンプトテンプレート集
X投稿用の図解・スライド画像を gemini-3.1-flash-image-preview で生成する。

テンプレート構造:
  [レイアウト], [ビジュアル要素], [日本語テキスト内容], [スタイル], [品質タグ]
"""

# ===================================================
# テンプレート1: リスト型スライド（箇条書き・番号付き）
# ===================================================
def list_slide(title: str, items: list[str], accent_color: str = "#2563EB") -> str:
    """
    タイトル＋箇条書きリストのスライド。
    例: 「7つのプロンプト」「5つのコツ」など。
    """
    items_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])
    return f"""
Single slide image, 16:9 aspect ratio, clean white background.

LAYOUT: Full-width title at top, numbered list below in 2 columns if 5+ items.
JAPANESE TEXT (render exactly):
  Title: 「{title}」
  Items:
{items_text}

STYLE:
- Title: bold, large font, color {accent_color}
- Items: medium font, dark gray, left-aligned
- Accent line under title in {accent_color}
- Subtle drop shadow on card
- Minimalist, professional

OUTPUT: High quality PNG, crisp Japanese text rendering, no English except icons.
""".strip()


# ===================================================
# テンプレート2: 比較型スライド（Before/After・左右対比）
# ===================================================
def compare_slide(title: str, left_label: str, left_items: list[str],
                  right_label: str, right_items: list[str]) -> str:
    """
    左右2カラムの比較スライド。Before/After・NG/OK など。
    """
    left_text = "\n".join([f"・{item}" for item in left_items])
    right_text = "\n".join([f"・{item}" for item in right_items])
    return f"""
Single slide image, 16:9 aspect ratio, white background.

LAYOUT: Two columns separated by vertical divider line.
JAPANESE TEXT (render exactly):
  Top title: 「{title}」
  Left column header: 「{left_label}」
  Left items:
{left_text}
  Right column header: 「{right_label}」
  Right items:
{right_text}

STYLE:
- Left header: red (#EF4444), bold
- Right header: green (#22C55E), bold
- Left background: light pink tint
- Right background: light green tint
- Clear divider line in center
- Professional, clean layout

OUTPUT: High quality PNG, crisp Japanese text rendering.
""".strip()


# ===================================================
# テンプレート3: フロー型スライド（矢印・ステップ）
# ===================================================
def flow_slide(title: str, steps: list[str], accent_color: str = "#7C3AED") -> str:
    """
    横並びステップ（→矢印）のフロースライド。
    """
    return f"""
Single slide image, 16:9 aspect ratio, white background.

LAYOUT: Horizontal flow with arrow connectors between {len(steps)} steps.
JAPANESE TEXT (render exactly):
  Title: 「{title}」
  Steps (left to right): {' → '.join(steps)}

STYLE:
- Each step in rounded rectangle box, color {accent_color}
- White text in step boxes, bold
- Large arrows (→) between boxes
- Title centered at top, dark color
- Step numbers (1,2,3...) above each box
- Clean, modern design

OUTPUT: High quality PNG, crisp Japanese text rendering.
""".strip()


# ===================================================
# テンプレート4: インサイト型スライド（1メッセージ強調）
# ===================================================
def insight_slide(main_message: str, sub_text: str = "", accent_color: str = "#F59E0B") -> str:
    """
    1つの強いメッセージを大きく見せるスライド。
    インパクト重視のX投稿用。
    """
    sub_part = f'\n  Subtitle: 「{sub_text}」' if sub_text else ""
    return f"""
Single slide image, 16:9 aspect ratio, dark background (#1E1E2E or deep navy).

LAYOUT: Centered, single large message. Minimal elements.
JAPANESE TEXT (render exactly):
  Main message (very large, bold): 「{main_message}」{sub_part}

STYLE:
- Background: dark (#1E1E2E)
- Main text: white or {accent_color}, very large (60-80pt equivalent)
- Accent underline or glow on key words
- Optional: subtle geometric shapes in background
- Dramatic, impactful design for social media

OUTPUT: High quality PNG, crisp Japanese text rendering.
""".strip()


# ===================================================
# 使用例・テスト
# ===================================================
if __name__ == "__main__":
    print("=== テンプレート1: リスト型 ===")
    print(list_slide(
        title="Gemini NanoBanana2で作れる図解7選",
        items=[
            "フロー図（工程・手順）",
            "比較表（Before/After）",
            "ピラミッド図（優先順位）",
            "マインドマップ",
            "タイムライン",
            "インフォグラフィック",
            "ダッシュボード風まとめ"
        ]
    ))

    print("\n=== テンプレート4: インサイト型 ===")
    print(insight_slide(
        main_message="AIに丸投げで\n図解が5秒で完成する時代",
        sub_text="プロンプト1行で誰でもデザイナーになれる"
    ))
