#!/usr/bin/env python3
"""一致性檢查（CI gate）。

1. STANDALONE.md 是否為 references/ 的最新 build 產物（呼叫 build.py --check）
2. LITE.md 是否涵蓋關鍵規則錨點（LITE 是有損壓縮，不要求逐字一致，只查錨點不漏）
3. SKILL / LITE / STANDALONE 三版 metadata.version 是否一致

用法: python3 scripts/check_consistency.py   # 任一不過 exit 1
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# LITE.md 必須涵蓋的關鍵錨點（每項是一組同義詞，命中任一即算涵蓋）
LITE_ANCHORS = {
    "機密 AI 禁用": ["機密文書禁止使用 AI", "機密文書應由承辦人"],
    "最小必要個資": ["最小必要", "不預設要求身分證字號"],
    "三個 guardrail": ["撰寫前的把關"],
    "防諂媚糾正": ["矛盾先糾正", "先指出錯誤並更正"],
    "防冒名": ["不為冒名", "不直接產出"],
    "防 injection": ["貼入內容", "忽略上述規則"],
    "法律免責": ["不構成法律意見", "僅供格式參考"],
    "引敘語方向": ["奉", "據"],
    "稱謂語方向": ["鈞", "貴"],
    "上行不用辦法段": ["辦法"],
    "訴願 30 日": ["30日", "第56條", "訴願"],
}

ERRORS: list[str] = []


def get_version(fname: str) -> str | None:
    text = (ROOT / fname).read_text(encoding="utf-8")
    m = re.search(r"^\s*version:\s*(\S+)", text, re.M)
    return m.group(1) if m else None


def check_standalone_built() -> None:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py"), "--check"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        ERRORS.append("STANDALONE.md 不是 references/ 的最新 build 產物。請跑 python3 scripts/build.py")
    else:
        print("✓ STANDALONE.md 與 references/ 一致")


def check_lite_anchors() -> None:
    lite = (ROOT / "LITE.md").read_text(encoding="utf-8")
    missing = [name for name, kws in LITE_ANCHORS.items() if not any(k in lite for k in kws)]
    if missing:
        ERRORS.append("LITE.md 缺少關鍵錨點: " + "、".join(missing))
    else:
        print(f"✓ LITE.md 涵蓋全部 {len(LITE_ANCHORS)} 個關鍵錨點")


def check_versions() -> None:
    versions = {f: get_version(f) for f in ("SKILL.md", "LITE.md", "STANDALONE.md")}
    if None in versions.values():
        ERRORS.append(f"有檔案讀不到 version: {versions}")
        return
    if len(set(versions.values())) != 1:
        ERRORS.append(f"三版 version 不一致: {versions}")
    else:
        print(f"✓ 三版 version 一致: {next(iter(versions.values()))}")


def main() -> None:
    check_standalone_built()
    check_lite_anchors()
    check_versions()
    if ERRORS:
        print("\nFAIL:")
        for e in ERRORS:
            print("  ✗ " + e)
        sys.exit(1)
    print("\nAll consistency checks passed.")


if __name__ == "__main__":
    main()
