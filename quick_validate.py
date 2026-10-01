#!/usr/bin/env python3
"""Validate a skill's SKILL.md structure (same rules as the Agent Skills quick_validate).

Usage: python quick_validate.py <skill_directory>
"""
import re
import sys
from pathlib import Path

import yaml

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def validate_skill(skill_path):
    skill_path = Path(skill_path)
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    content = skill_md.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return False, "No YAML frontmatter found"

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format"

    frontmatter_text = match.group(1)
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except yaml.YAMLError as e:
        return False, "Invalid YAML in frontmatter: %s" % e

    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        return False, "Unexpected key(s) in frontmatter: %s. Allowed: %s" % (
            ", ".join(sorted(unexpected)),
            ", ".join(sorted(ALLOWED_PROPERTIES)),
        )

    if "name" not in frontmatter:
        return False, "Missing 'name' in frontmatter"
    if "description" not in frontmatter:
        return False, "Missing 'description' in frontmatter"

    name = frontmatter.get("name", "")
    if not isinstance(name, str):
        return False, "Name must be a string, got %s" % type(name).__name__
    name = name.strip()
    if name:
        if not re.match(r"^[a-z0-9-]+$", name):
            return False, "Name '%s' should be hyphen-case (lowercase letters, digits, hyphens only)" % name
        if name.startswith("-") or name.endswith("-") or "--" in name:
            return False, "Name '%s' cannot start/end with hyphen or contain consecutive hyphens" % name
        if len(name) > MAX_SKILL_NAME_LENGTH:
            return False, "Name is too long (%d chars). Max is %d." % (len(name), MAX_SKILL_NAME_LENGTH)

    description = frontmatter.get("description", "")
    if not isinstance(description, str):
        return False, "Description must be a string, got %s" % type(description).__name__
    description = description.strip()
    if description:
        if "<" in description or ">" in description:
            return False, "Description cannot contain angle brackets (< or >)"
        if len(description) > 1024:
            return False, "Description is too long (%d chars). Max is 1024." % len(description)

    return True, "Skill is valid!"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill_directory>")
        sys.exit(1)
    ok, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if ok else 1)
