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
        cls.valid_data = json.loads(DEFAULT_SIGNAL.read_text(encoding="utf-8"))
        cls.template = DEFAULT_TEMPLATE.read_text(encoding="utf-8")

    def test_provisional_signal_renders_ef001_without_mutating_template(self):
        original = self.template
        svg = render_svg(original, validate_signal(copy.deepcopy(self.valid_data)))
        self.assertIn(">PROVISIONAL</text>", svg)
        self.assertIn("EF-001 · Public orientation claim", svg)
        self.assertIn("SOURCE  /  EF-001 · 2026-11-20", svg)
        self.assertIn("MG–001   /   v0.2", svg)
        self.assertEqual(original, self.template)
        self.assertIn(">UNVERIFIED</text>", self.template)

    def test_explicit_unknown_stays_visibly_unknown(self):
        data = copy.deepcopy(self.valid_data)
        data["state"] = "unknown"
        svg = render_svg(self.template, validate_signal(data))
        self.assertIn(">UNKNOWN</text>", svg)
        self.assertNotIn(">PROVISIONAL</text>", svg)

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
