#!/usr/bin/env python3
"""一致性檢查（CI gate）。

1. 三項生成產物是否為最新（呼叫 build.py --check）：
   STANDALONE.md / skills/tw-formal-writing/ / AGENTS.md·GEMINI.md
2. LITE.md 是否涵蓋關鍵規則錨點（LITE 是有損壓縮，不要求逐字一致，只查錨點不漏）
3. 五處 version 是否一致（SKILL / LITE / STANDALONE / plugin.json / marketplace.json）
4. skill 包打包清單齊全（package.py 要打進 zip 的檔都在，避免誤刪 examples/ 或 LICENSE）

用法: python3 scripts/check_consistency.py   # 任一不過 exit 1
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import package  # 複用 collect_files() 驗打包清單（單一真實來源，不重寫規則）

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
        ERRORS.append(
            "生成產物過期，請跑 python3 scripts/build.py\n    " + r.stdout.strip().replace("\n", "\n    ")
        )
    else:
        print("✓ 三項生成產物皆為最新（STANDALONE.md / skills/ / AGENTS.md·GEMINI.md）")


def check_lite_anchors() -> None:
    lite = (ROOT / "LITE.md").read_text(encoding="utf-8")
    missing = [name for name, kws in LITE_ANCHORS.items() if not any(k in lite for k in kws)]
    if missing:
        ERRORS.append("LITE.md 缺少關鍵錨點: " + "、".join(missing))
    else:
        print(f"✓ LITE.md 涵蓋全部 {len(LITE_ANCHORS)} 個關鍵錨點")


def check_package_manifest() -> None:
    """skill 包（package.py 打進 zip 的檔）清單齊全：SKILL / references / examples / LICENSE。

    直接複用 package.collect_files()——同一份清單邏輯，package.py 若改打包內容，這裡自動跟上，
    不會漂移。差別只在失敗處理：package 的 CLI 端 sys.exit，這裡收斂成 ERRORS 統一報告。
    抓的是「誤刪整組」的情況（例如 examples/ 或 LICENSE 不見）。
    """
    _, errors = package.collect_files()
    if errors:
        ERRORS.append("skill 包打包清單缺檔: " + "、".join(errors))
    else:
        print("✓ skill 包打包清單齊全（SKILL / references / examples / LICENSE）")


def check_versions() -> None:
    """五個 version 同步點：三份 markdown + plugin.json + marketplace.json 的 plugin entry。

    後兩者是 Claude Code plugin / marketplace 安裝時顯示給使用者的版本號，跟內容版本
    漂移的話，安裝者會拿到「掛著舊版號的新內容」。SKILL.md 是源頭。
    """
    versions = {f: get_version(f) for f in ("SKILL.md", "LITE.md", "STANDALONE.md")}

    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    versions[".claude-plugin/plugin.json"] = plugin.get("version")

    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")]
    if not entries:
        ERRORS.append(f"marketplace.json 沒有 name 為 {plugin.get('name')!r} 的 plugin entry")
        return
    versions["marketplace.json[tw-formal-writing]"] = entries[0].get("version")

    if None in versions.values():
        ERRORS.append(f"有檔案讀不到 version: {versions}")
        return
    if len(set(versions.values())) != 1:
        ERRORS.append(f"五處 version 不一致: {versions}")
    else:
        print(f"✓ 五處 version 一致: {next(iter(versions.values()))}")


def main() -> None:
    check_standalone_built()
    check_lite_anchors()
    check_package_manifest()
    check_versions()
    if ERRORS:
        print("\nFAIL:")
        for e in ERRORS:
            print("  ✗ " + e)
        sys.exit(1)
    print("\nAll consistency checks passed.")


if __name__ == "__main__":
    main()
