"""Keep the public orientation aligned with the claim assessed in EF-001."""
import re
import unittest
from pathlib import Path

PROFILE = Path(__file__).resolve().parents[2] / "profile"


class ProfileTests(unittest.TestCase):
    def test_assessed_claim_appears_in_its_declared_section(self):
        record = (PROFILE / "META-GAUGE.md").read_text(encoding="utf-8")
        profile = (PROFILE / "README.md").read_text(encoding="utf-8")
        claim = re.search(r"^\*\*Source statement:\*\*[^\n]+\n\n> ([^\n]+)", record, re.M)
        self.assertIsNotNone(claim, "Missing EF-001 source quotation")
        orientation = profile.split("## I. Orientation\n", 1)[1].split("\n## ", 1)[0]
        self.assertIn(claim.group(1), orientation.splitlines())
