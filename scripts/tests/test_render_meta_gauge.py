import copy
import json
import struct
import tempfile
import unittest
from pathlib import Path

from scripts.render_meta_gauge import (
    DEFAULT_SIGNAL,
    DEFAULT_TEMPLATE,
    SignalValidationError,
    generate,
    load_signal,
    render_png,
    render_svg,
    validate_signal,
)


class MetaGaugeRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Keep expected outcomes independent of the live assessment.
        cls.valid_data = {
            "schema_version": 1,
            "instrument": "MG-001",
            "id": "EF-001",
            "register": "epistemic-fix",
            "scope": "public-research-orientation",
            "state": "provisionally-supported",
            "assessed_at": "2025-01-15",
            "assessment_type": "manual-source-comparison",
            "evidence_visibility": "private",
            "authority_verified": False,
            "display_authority": "display-only",
        }
        cls.template = DEFAULT_TEMPLATE.read_text(encoding="utf-8")

    def test_repository_signal_validates(self):
        load_signal(DEFAULT_SIGNAL)

    def test_provisional_signal_renders_ef001_without_mutating_template(self):
        original = self.template
        svg = render_svg(original, validate_signal(copy.deepcopy(self.valid_data)))
        self.assertIn(">PROVISIONAL</text>", svg)
        self.assertIn("EF-001 · Public orientation claim", svg)
        self.assertIn("SOURCE  /  EF-001 · 2025-01-15", svg)
        self.assertIn("MG–001   /   v0.2", svg)
        self.assertEqual(original, self.template)
        self.assertIn(">UNVERIFIED</text>", self.template)

    def test_explicit_unknown_stays_visibly_unknown(self):
        data = copy.deepcopy(self.valid_data)
        data["state"] = "unknown"
        svg = render_svg(self.template, validate_signal(data))
        self.assertIn(">UNKNOWN</text>", svg)
        self.assertNotIn(">PROVISIONAL</text>", svg)

    def test_signal_updates_regenerate_svg_and_png(self):
        cases = (
            ({"assessed_at": "2025-02-01"}, ">PROVISIONAL</text>", "2025-02-01"),
            ({"state": "unknown"}, ">UNKNOWN</text>", "2025-01-15"),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            signal_path = root / "signal.json"
            svg_path = root / "current.svg"
            png_path = root / "current.png"
            signal_path.write_text(json.dumps(self.valid_data), encoding="utf-8")
            generate(signal_path, DEFAULT_TEMPLATE, svg_path, png_path)
            original_png = png_path.read_bytes()

            for update, expected_status, expected_date in cases:
                with self.subTest(update=update):
                    signal_path.write_text(
                        json.dumps(self.valid_data | update), encoding="utf-8"
                    )
                    generate(signal_path, DEFAULT_TEMPLATE, svg_path, png_path)
                    svg = svg_path.read_text(encoding="utf-8")
                    png = png_path.read_bytes()
                    self.assertIn(expected_status, svg)
                    self.assertIn(f"SOURCE  /  EF-001 · {expected_date}", svg)
                    self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                    self.assertNotEqual(png, original_png)

    def test_unknown_state_is_rejected_instead_of_becoming_confident(self):
        data = copy.deepcopy(self.valid_data)
        data["state"] = "probably-supported"
        with self.assertRaisesRegex(SignalValidationError, "unknown state"):
            validate_signal(data)

    def test_missing_field_is_rejected(self):
        data = copy.deepcopy(self.valid_data)
        del data["authority_verified"]
        with self.assertRaisesRegex(SignalValidationError, "missing required fields"):
            validate_signal(data)

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "signal.json"
            path.write_text('{"state":', encoding="utf-8")
            with self.assertRaisesRegex(SignalValidationError, "invalid JSON"):
                load_signal(path)

    def test_invalid_signal_does_not_replace_existing_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            signal_path = root / "signal.json"
            template_path = root / "template.svg"
            svg_path = root / "current.svg"
            png_path = root / "current.png"

            invalid = copy.deepcopy(self.valid_data)
            invalid["state"] = "confident-but-undefined"
            signal_path.write_text(json.dumps(invalid), encoding="utf-8")
            template_path.write_text(self.template, encoding="utf-8")
            svg_path.write_bytes(b"existing svg")
            png_path.write_bytes(b"existing png")

            with self.assertRaises(SignalValidationError):
                generate(signal_path, template_path, svg_path, png_path)

            self.assertEqual(svg_path.read_bytes(), b"existing svg")
            self.assertEqual(png_path.read_bytes(), b"existing png")

    def test_svg_is_deterministic(self):
        signal = validate_signal(copy.deepcopy(self.valid_data))
        self.assertEqual(
            render_svg(self.template, signal),
            render_svg(self.template, signal),
        )

    def test_mobile_png_has_expected_signature_and_dimensions(self):
        signal = validate_signal(copy.deepcopy(self.valid_data))
        svg = render_svg(self.template, signal).encode("utf-8")
        png = render_png(svg)
        self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
        width, height = struct.unpack(">II", png[16:24])
        self.assertEqual((width, height), (960, 360))


if __name__ == "__main__":
    unittest.main()
