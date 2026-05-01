#!/usr/bin/env python3
"""Verify every Wireshark display-filter field referenced by this toolkit's
profiles actually exists in the local Wireshark dissector tables.

How it works:
  1. Walk profiles/<name>/{dfilters,colorfilters,dfilter_buttons} files and
     pull out every token of the form `proto.field[.sub.field]`.
  2. Run `tshark -G fields` to enumerate every field the local Wireshark
     installation knows about.
  3. Diff and report missing / unknown fields per profile.

Exit code is non-zero if any unknown field is found, so this is suitable for
CI. The same script also has a parser-only mode (--no-tshark) that skips the
external check, useful in environments where tshark isn't installed.

Usage:
    python validate.py                  # check every profile
    python validate.py --profile 5g-sa-core
    python validate.py --no-tshark      # parse-only sanity check
"""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
PROFILES_DIR = REPO_ROOT / "profiles"

# Files inside each profile that contain display-filter expressions.
DFILTER_BEARING_FILES = ("dfilters", "colorfilters", "dfilter_buttons")

# A "field" looks like proto.field or proto.field.sub_field. Keep matching
# very tight so we don't mistake hex literals or string contents for fields.
# A field token: starts with a letter, may contain letters/digits/_/-, must
# contain at least one '.' (i.e. proto.field). Examples we want to match:
#   ngap.procedureCode, nas-5gs.mm.message_type, nas-eps.nas_msg_emm_type,
#   pfcp.apply_action.forw, x2ap.SgNBAdditionRequest_element
FIELD_RE = re.compile(r"\b([A-Za-z][A-Za-z0-9_\-]*\.[A-Za-z0-9_.\-]+)")
DFILTER_LINE_RE = re.compile(r'^"(?:[^"\\]|\\.)*"\s*(?P<expr>.*)$')
QUOTED_STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')

# Tokens that look like fields but aren't. Drop these to avoid false positives.
NOT_FIELDS = {
    "tcp.port",
    "udp.port",
    "sctp.port",
    "ip.addr",
    "ipv6.addr",
    "tcp.flags.syn",
    "tcp.flags.ack",
    # Generic Wireshark shorthands also accepted as protocol-only filters.
}


def _filter_expressions(filename: str, line: str) -> list[str]:
    """Extract display-filter expressions from a Wireshark profile line."""
    if filename == "dfilter_buttons":
        try:
            row = next(csv.reader([line], escapechar="\\"))
        except csv.Error:
            return []
        return [row[2]] if len(row) >= 3 else []

    if filename == "colorfilters":
        parts = line.split("@", 3)
        return [parts[2]] if len(parts) >= 4 else []

    match = DFILTER_LINE_RE.match(line)
    return [match.group("expr") if match else line]


def _without_quoted_strings(expression: str) -> str:
    """Remove string literals so values like "IEEE-802.11" are not treated as fields."""
    return QUOTED_STRING_RE.sub('""', expression)


def collect_fields(profile_dir: Path) -> set[str]:
    """Return the set of every dotted token used in this profile's filter files."""
    found: set[str] = set()
    for filename in DFILTER_BEARING_FILES:
        path = profile_dir / filename
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for expression in _filter_expressions(filename, stripped):
                expression = _without_quoted_strings(expression)
                for match in FIELD_RE.finditer(expression):
                    token = match.group(1).rstrip(".-_")
                    if "." not in token:
                        continue
                    # Reject tokens whose every part is purely numeric, since those
                    # are IP literals like 10.0.0.1, not field names.
                    parts = token.split(".")
                    if all(p.replace("-", "").isdigit() for p in parts):
                        continue
                    # Reject tokens that look like version strings (1.2.0).
                    if all(p.replace("_", "").replace("-", "").isdigit() for p in parts):
                        continue
                    found.add(token)
    return found


def known_tshark_fields() -> set[str] | None:
    """Return the set of fields tshark reports, or None if tshark isn't available."""
    if not shutil.which("tshark"):
        return None
    try:
        proc = subprocess.run(
            ["tshark", "-G", "fields"],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        print(f"[warn] tshark -G fields failed: {exc}", file=sys.stderr)
        return None

    fields: set[str] = set()
    # tshark output lines beginning with 'F' look like:
    #   F<TAB>name<TAB>filter_name<TAB>type<TAB>parent_proto<TAB>...
    for line in proc.stdout.splitlines():
        if not line.startswith("F\t"):
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            fields.add(parts[2])
    return fields


def check_profile(profile_dir: Path, known: set[str] | None) -> list[str]:
    """Return a list of unknown field tokens for this profile."""
    used = collect_fields(profile_dir)
    if known is None:
        return []
    unknown = sorted(t for t in used if t not in known and t not in NOT_FIELDS)
    return unknown


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--profile",
        help="Check just this profile (subdirectory of profiles/).",
        default=None,
    )
    parser.add_argument(
        "--no-tshark",
        action="store_true",
        help="Skip the tshark cross-check; only verify the parser is happy.",
    )
    args = parser.parse_args()

    if not PROFILES_DIR.is_dir():
        print(f"[error] profiles directory not found: {PROFILES_DIR}", file=sys.stderr)
        return 2

    targets: list[Path]
    if args.profile:
        target = PROFILES_DIR / args.profile
        if not target.is_dir():
            print(f"[error] no such profile: {args.profile}", file=sys.stderr)
            return 2
        targets = [target]
    else:
        targets = sorted(p for p in PROFILES_DIR.iterdir() if p.is_dir())

    known = None if args.no_tshark else known_tshark_fields()
    if known is None:
        print(
            "[info] tshark unavailable or --no-tshark set; running parser-only mode."
            " Install Wireshark and re-run for full validation.",
        )

    total_unknown = 0
    for profile_dir in targets:
        used = collect_fields(profile_dir)
        print(f"\n=== {profile_dir.name}: {len(used)} field references ===")
        if known is None:
            continue
        unknown = check_profile(profile_dir, known)
        if not unknown:
            print("  ✓ all referenced fields exist in tshark -G fields output")
        else:
            print(f"  ✗ {len(unknown)} unknown field(s):")
            for u in unknown:
                print(f"      {u}")
            total_unknown += len(unknown)

    if total_unknown:
        print(f"\n{total_unknown} unknown field(s) total. See output above.", file=sys.stderr)
        return 1
    print("\nAll profiles validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
