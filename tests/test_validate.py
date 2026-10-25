"""Unit tests for quick_validate.valid_skill."""

from pathlib import Path

import quick_validate

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "make-knowledge-cards"


def write_skill(tmp_path, content):
    skill = tmp_path / "skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text(content, encoding="utf-8")
    return skill


def test_real_skill_is_valid():
    ok, message = quick_validate.validate_skill(str(SKILL_DIR))
    assert ok, message


def test_missing_skill_md(tmp_path):
    ok, message = quick_validate.validate_skill(str(tmp_path))
    assert not ok
    assert "SKILL.md not found" in message


def test_no_frontmatter(tmp_path):
    skill = write_skill(tmp_path, "# 没有 frontmatter\n")
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "frontmatter" in message


def test_invalid_yaml(tmp_path):
    skill = write_skill(tmp_path, "---\nname: [unclosed\n---\n")
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "YAML" in message


def test_missing_name_and_description(tmp_path):
    skill = write_skill(tmp_path, "---\nlicense: MIT\n---\n正文\n")
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "name" in message


def test_bad_name_characters(tmp_path):
    skill = write_skill(
        tmp_path,
        "---\nname: Not_Hyphen_Case\ndescription: 一个技能\n---\n正文\n",
    )
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "hyphen-case" in message


def test_description_with_angle_brackets(tmp_path):
    skill = write_skill(
        tmp_path,
        "---\nname: demo-skill\ndescription: 用 <tag> 的说明\n---\n正文\n",
    )
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "angle brackets" in message


def test_unexpected_frontmatter_key(tmp_path):
    skill = write_skill(
        tmp_path,
        "---\nname: demo-skill\ndescription: 说明\nbogus: 1\n---\n正文\n",
    )
    ok, message = quick_validate.validate_skill(str(skill))
    assert not ok
    assert "Unexpected key" in message


def test_valid_minimal_skill(tmp_path):
    skill = write_skill(
        tmp_path,
        "---\nname: demo-skill\ndescription: 一个合法的技能\n---\n# 标题\n正文\n",
    )
    ok, message = quick_validate.validate_skill(str(skill))
    assert ok, message
