#!/usr/bin/env python3
"""
Tests for quick_validate.validate_skill.

Uses the stdlib `unittest` runner so it executes in environments without pytest:
    python3 -m scripts.test_quick_validate     # from the skill root
    python3 scripts/test_quick_validate.py     # direct
"""
import sys
import tempfile
import unittest
from pathlib import Path

# Allow both `python3 -m scripts.test_quick_validate` and direct execution.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quick_validate import validate_skill  # noqa: E402


def write_skill(tmp: Path, frontmatter: str, body: str = "\n# Body\n") -> Path:
    skill_dir = tmp / "skill"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text(f"---\n{frontmatter}\n---{body}")
    return skill_dir


class TestValidateSkill(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_valid_skill(self):
        d = write_skill(self.tmp, "name: my-skill\ndescription: Use when testing the validator.")
        ok, msg = validate_skill(d)
        self.assertTrue(ok, msg)

    def test_missing_skill_md(self):
        empty = self.tmp / "empty"
        empty.mkdir()
        ok, msg = validate_skill(empty)
        self.assertFalse(ok)
        self.assertIn("SKILL.md not found", msg)

    def test_no_frontmatter(self):
        d = self.tmp / "skill"
        d.mkdir()
        (d / "SKILL.md").write_text("# Just a heading, no frontmatter\n")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)

    def test_unexpected_keys_rejected(self):
        d = write_skill(
            self.tmp,
            "name: my-skill\ndescription: Valid description.\ncowork: true\nstatus: active",
        )
        ok, msg = validate_skill(d)
        self.assertFalse(ok)
        self.assertIn("cowork", msg)
        self.assertIn("status", msg)

    def test_missing_name(self):
        d = write_skill(self.tmp, "description: Has a description but no name.")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)
        self.assertIn("name", msg)

    def test_bad_name_not_kebab(self):
        d = write_skill(self.tmp, "name: My_Skill\ndescription: Valid description.")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)
        self.assertIn("kebab", msg.lower())

    def test_consecutive_hyphens_rejected(self):
        d = write_skill(self.tmp, "name: my--skill\ndescription: Valid description.")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)

    def test_angle_brackets_in_description(self):
        d = write_skill(self.tmp, "name: my-skill\ndescription: Use when <tag> appears.")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)
        self.assertIn("angle bracket", msg.lower())

    def test_description_too_long(self):
        long_desc = "x" * 1025
        d = write_skill(self.tmp, f"name: my-skill\ndescription: {long_desc}")
        ok, msg = validate_skill(d)
        self.assertFalse(ok)
        self.assertIn("too long", msg.lower())

    def test_metadata_key_allowed(self):
        d = write_skill(
            self.tmp,
            "name: my-skill\ndescription: Valid description.\nmetadata:\n  author: erman",
        )
        ok, msg = validate_skill(d)
        self.assertTrue(ok, msg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
