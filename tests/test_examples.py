"""Validate the examples/ directory: every article has a .cards.md, and each cards file follows the template."""

import re
from pathlib import Path

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"

FIELDS = ("核心知识", "简明解释", "例子 / 自测")
CARD_HEADING = re.compile(r"^### 卡片 \d+：", re.MULTILINE)


def card_files():
    return sorted(EXAMPLES_DIR.glob("*.cards.md"))


def test_every_article_has_cards():
    card_stems = {p.name.replace(".cards.md", "") for p in EXAMPLES_DIR.glob("*.cards.md")}
    articles = [p for p in sorted(EXAMPLES_DIR.glob("*.md")) if not p.name.endswith(".cards.md")]
    assert articles, "no example articles found"
    for article in articles:
        assert article.stem in card_stems, f"{article.name} has no matching .cards.md"


def test_cards_have_expected_structure():
    for cards_file in card_files():
        text = cards_file.read_text(encoding="utf-8")
        assert CARD_HEADING.search(text), f"{cards_file.name} is missing '### 卡片 N：' sections"
        for field in FIELDS:
            assert f"**{field}**" in text, f"{cards_file.name} is missing the '{field}' field"


def test_card_count_within_bounds():
    for cards_file in card_files():
        text = cards_file.read_text(encoding="utf-8")
        count = len(CARD_HEADING.findall(text))
        assert 1 <= count <= 8, f"{cards_file.name} has {count} cards, expected 1-8"
