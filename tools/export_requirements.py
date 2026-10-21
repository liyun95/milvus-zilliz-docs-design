#!/usr/bin/env python3
"""Export the checkable requirement IDs of Phase 1 into one JSON file.

Reads the PRD (numbered system behaviours such as ``4-3``), the Phase 1 plan
(acceptance tests ``T01``–``T14``) and the error catalog (error codes), and
writes ``docs/implementation/requirements.json``. Implementation repositories copy
that file and check that every ID is covered by at least one test.

Usage:
    python3 tools/export_requirements.py           # write the file
    python3 tools/export_requirements.py --check   # fail if the file is stale
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRD = ROOT / "docs" / "prd.md"
PLAN = ROOT / "docs" / "phase-1.md"
ERRORS = ROOT / "docs" / "design" / "09-error-catalog.md"
OUTPUT = ROOT / "docs" / "implementation" / "requirements.json"

SCENARIO_HEADING = re.compile(r"^### 场景 (\d+)：(.+)$")
PHASE_LINE = re.compile(r"^\*\*阶段\*\*：(Phase 1[ab])")
BEHAVIOUR_ROW = re.compile(r"^\| (\d{1,2}-\d{1,2}) \| (.+?) \|\s*$")
ACCEPTANCE_ITEM = re.compile(r"^- 【(T\d{2})】(.+)$")
BLOCKING_LINE = re.compile(r"(T\d{2}(?:、T\d{2})*) 是上线阻断项")
ERROR_SECTION = re.compile(r"^\*\*(.+?)\*\*（")
ERROR_ROW = re.compile(r"^\| `([A-Z][A-Z0-9_]+)` \| (.+?) \|")
ERROR_INLINE = re.compile(r"`([A-Z][A-Z0-9_]{3,})`")


def read(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise SystemExit(f"cannot read {path}: {error}") from error


def behaviours() -> list[dict]:
    items, scenario, title, phase = [], None, None, None
    for line in read(PRD):
        if match := SCENARIO_HEADING.match(line):
            scenario, title, phase = int(match[1]), match[2], None
        elif match := PHASE_LINE.match(line):
            phase = match[1]
        elif scenario and (match := BEHAVIOUR_ROW.match(line)):
            if not match[1].startswith(f"{scenario}-"):
                raise SystemExit(f"behaviour {match[1]} appears under scenario {scenario}")
            items.append({"id": match[1], "scenario": scenario, "scenario_title": title,
                          "phase": phase, "text": match[2]})
    ids = [item["id"] for item in items]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        raise SystemExit(f"duplicate behaviour IDs in PRD: {duplicates}")
    return items


def acceptance() -> list[dict]:
    lines = read(PLAN)
    blocking = set()
    for line in lines:
        if match := BLOCKING_LINE.search(line):
            blocking.update(match[1].split("、"))
    items = [{"id": m[1], "text": m[2].strip(), "blocking": m[1] in blocking}
             for line in lines if (m := ACCEPTANCE_ITEM.match(line))]
    return sorted({item["id"]: item for item in items}.values(), key=lambda item: item["id"])


def errors() -> list[dict]:
    items, area = {}, None
    for line in read(ERRORS):
        if match := ERROR_SECTION.match(line):
            area = match[1]
            # Areas whose codes are listed inline, e.g. the named-block codes.
            for code in ERROR_INLINE.findall(line):
                items.setdefault(code, {"code": code, "area": area, "when": ""})
        elif match := ERROR_ROW.match(line):
            items[match[1]] = {"code": match[1], "area": area, "when": match[2]}
        elif line.startswith("提升时不符合条件"):
            for code in ERROR_INLINE.findall(line):
                items.setdefault(code, {"code": code, "area": "提升", "when": "运行摘要中列出，不算错误"})
    return list(items.values())


def prd_commit() -> str:
    result = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%H", "--", "docs/prd.md"],
                            capture_output=True, text=True, check=False)
    return result.stdout.strip() or "uncommitted"


def build() -> dict:
    return {
        "schema_version": 1,
        "generated_by": "tools/export_requirements.py",
        "source": {"prd": "docs/prd.md", "plan": "docs/phase-1.md",
                   "errors": "docs/design/09-error-catalog.md", "prd_commit": prd_commit()},
        "behaviours": behaviours(),
        "acceptance": acceptance(),
        "errors": errors(),
    }


def main() -> None:
    data = build()
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if "--check" in sys.argv:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        strip = lambda s: re.sub(r'"prd_commit": "[^"]*"', "", s)
        if strip(current) != strip(text):
            raise SystemExit(f"{OUTPUT.relative_to(ROOT)} is stale; run tools/export_requirements.py")
        return
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"{OUTPUT.relative_to(ROOT)}: {len(data['behaviours'])} behaviours, "
          f"{len(data['acceptance'])} acceptance tests, {len(data['errors'])} error codes")


if __name__ == "__main__":
    main()
