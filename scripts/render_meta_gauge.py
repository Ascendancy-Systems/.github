#!/usr/bin/env python3
"""Render the MG-001 public display from one validated signal record.

The original v0.1 SVG remains the visual source. This renderer applies a
small, deterministic set of text substitutions and then creates a mobile PNG.
Invalid records fail before either generated asset is replaced.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SIGNAL = ROOT / "profile/signals/meta-gauge-mg-001.json"
DEFAULT_TEMPLATE = ROOT / "profile/assets/meta-gauge-v0.1.svg"
DEFAULT_SVG = ROOT / "profile/assets/meta-gauge-current.svg"
DEFAULT_PNG = ROOT / "profile/assets/meta-gauge-current.png"

EXPECTED_KEYS = {
    "schema_version",
    "instrument",
    "id",
    "register",
    "scope",
    "state",
    "assessed_at",
    "assessment_type",
    "evidence_visibility",
    "authority_verified",
    "display_authority",
}

STATE_DISPLAYS = {
    "provisionally-supported": ("PROVISIONAL", "#D6DCE3"),
    "supported": ("SUPPORTED", "#D6DCE3"),
    "unsupported": ("NOT SUPPORTED", "#C98C82"),
    "unverified": ("UNVERIFIED", "#D6DCE3"),
    "unknown": ("UNKNOWN", "#D6DCE3"),
}


class SignalValidationError(ValueError):
    """Raised when a signal cannot safely authorize a display reading."""


@dataclass(frozen=True)
class Signal:
    schema_version: int
    instrument: str
    id: str
    register: str
    scope: str
    state: str
    assessed_at: str
    assessment_type: str
    evidence_visibility: str
    authority_verified: bool
    display_authority: str

    @property
    def display_state(self) -> str:
        return STATE_DISPLAYS[self.state][0]

    @property
    def display_colour(self) -> str:
        return STATE_DISPLAYS[self.state][1]


def _require_type(data: dict[str, Any], key: str, expected: type) -> Any:
    value = data[key]
    if type(value) is not expected:  # bool is intentionally not accepted as int
        raise SignalValidationError(f"{key!r} must be {expected.__name__}")
    return value


def validate_signal(data: Any) -> Signal:
    if not isinstance(data, dict):
        raise SignalValidationError("signal must be a JSON object")

    keys = set(data)
    missing = EXPECTED_KEYS - keys
    unexpected = keys - EXPECTED_KEYS
    if missing:
        raise SignalValidationError(f"missing required fields: {', '.join(sorted(missing))}")
    if unexpected:
        raise SignalValidationError(f"unexpected fields: {', '.join(sorted(unexpected))}")

    schema_version = _require_type(data, "schema_version", int)
    text_values = {
        key: _require_type(data, key, str)
        for key in EXPECTED_KEYS - {"schema_version", "authority_verified"}
    }
    authority_verified = _require_type(data, "authority_verified", bool)

    if schema_version != 1:
        raise SignalValidationError("schema_version must be 1")
    fixed_values = {
        "instrument": "MG-001",
        "id": "EF-001",
        "register": "epistemic-fix",
        "scope": "public-research-orientation",
        "assessment_type": "manual-source-comparison",
        "evidence_visibility": "private",
        "display_authority": "display-only",
    }
    for key, expected in fixed_values.items():
        if text_values[key] != expected:
            raise SignalValidationError(f"{key!r} must be {expected!r}")

    state = text_values["state"]
    if state not in STATE_DISPLAYS:
        raise SignalValidationError(
            f"unknown state {state!r}; use one of: {', '.join(sorted(STATE_DISPLAYS))}"
        )

    assessed_at = text_values["assessed_at"]
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", assessed_at):
        raise SignalValidationError("assessed_at must use YYYY-MM-DD")
    try:
        date.fromisoformat(assessed_at)
    except ValueError as exc:
        raise SignalValidationError("assessed_at must be a real calendar date") from exc

    return Signal(
        schema_version=schema_version,
        authority_verified=authority_verified,
        **text_values,
    )


def load_signal(path: Path) -> Signal:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SignalValidationError(f"signal file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SignalValidationError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc
    return validate_signal(data)


def _replace_once(source: str, old: str, new: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"template marker must occur once, found {count}: {old[:72]!r}")
    return source.replace(old, new, 1)


def render_svg(template: str, signal: Signal) -> str:
    """Return a byte-stable SVG for a validated signal and template."""
    title = f"{signal.id} · Public orientation claim"
    footer_source = f"SOURCE  /  {signal.id} · {signal.assessed_at}"

    replacements = (
        (
            "A static public-orientation instrument. A hollow gold eight-pointed star",
            "A source-driven public-orientation instrument. A hollow gold eight-pointed star",
        ),
        ("MG–001   /   v0.1", "MG–001   /   v0.2"),
        (
            '<text x="97" y="400" fill="#D6DCE3" font-size="26"',
            f'<text x="97" y="400" fill="{signal.display_colour}" font-size="26"',
        ),
        (
            '>UNVERIFIED</text>\n<text x="97" y="432"',
            f'>{signal.display_state}</text>\n<text x="97" y="432"',
        ),
        (">Claim / evidence audit pending</text>", f">{title}</text>"),
        (">DISPLAY  /  STATIC</text>", ">DISPLAY  /  GENERATED</text>"),
        (">SIGNALS  /  UNCONNECTED</text>", ">SIGNALS  /  EF-001 CONNECTED</text>"),
        (">SOURCE  /  REGISTRY PENDING</text>", f">{footer_source}</text>"),
    )

    rendered = template
    for old, new in replacements:
        rendered = _replace_once(rendered, old, new)

    return "<!-- Generated by scripts/render_meta_gauge.py; do not edit directly. -->\n" + rendered


def render_png(svg_bytes: bytes, width: int = 960) -> bytes:
    try:
        import cairosvg
    except ImportError as exc:
        raise RuntimeError(
            "PNG rendering requires requirements-meta-gauge.txt"
        ) from exc
    return cairosvg.svg2png(bytestring=svg_bytes, output_width=width)


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def generate(signal_path: Path, template_path: Path, svg_path: Path, png_path: Path) -> None:
    signal = load_signal(signal_path)
    template = template_path.read_text(encoding="utf-8")
    svg_bytes = render_svg(template, signal).encode("utf-8")
    png_bytes = render_png(svg_bytes)

    # Both outputs are prepared before either current asset is replaced.
    _atomic_write(svg_path, svg_bytes)
    _atomic_write(png_path, png_bytes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--signal", type=Path, default=DEFAULT_SIGNAL)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--svg", type=Path, default=DEFAULT_SVG)
    parser.add_argument("--png", type=Path, default=DEFAULT_PNG)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        generate(args.signal, args.template, args.svg, args.png)
    except (SignalValidationError, RuntimeError, OSError) as exc:
        print(f"Meta-Gauge render refused: {exc}")
        return 2
    print(f"Rendered {args.svg} and {args.png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
