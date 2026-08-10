#!/usr/bin/env python3
"""從 source 檔組裝 STANDALONE.md，並鏡射 plugin skill 目錄。

Single source of truth:
- frontmatter version 取自 SKILL.md
- 頭部(類別判斷/把關/共通原則/互動流程)= references/_header.md
- 五個附錄 = references/*.md(各自降級成「附錄N」標題)

三項生成產物，都不應手動編輯，改規範請改 references/：
- STANDALONE.md：單檔完整版(ChatGPT / Claude Project 上傳用)
- skills/tw-formal-writing/：Claude Code plugin 的 skill 目錄，內容鏡射自
  SKILL.md + references/ + examples/
- AGENTS.md / GEMINI.md：Codex / Gemini CLI 的自動讀取入口，內容即 STANDALONE.md

用法: python3 scripts/build.py        # 寫出全部三項生成產物
      python3 scripts/build.py --check # 只檢查是否與現檔一致(CI 用)，不一致則 exit 1
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
EXAMPLES = ROOT / "examples"
OUT = ROOT / "STANDALONE.md"

# Claude Code plugin 的 skill 目錄。官方規格要求 SKILL.md 與它引用的 references/、
# examples/ 同層(見 plugin-dev/plugin-structure)，而 SSOT 在 repo 根目錄，故此處放
# 實體複本而非 symlink——plugin 安裝走 git clone，Windows 預設不還原 symlink。
PLUGIN_SKILL = ROOT / "skills" / "tw-formal-writing"

# 其他 vendor 的自動讀取入口，內容即 STANDALONE.md。同樣是實體複本而非 symlink：
# 這兩個檔是給人 clone repo 後直接用的，Windows 的 git 預設 core.symlinks=false，
# 會把 symlink 還原成一行純文字路徑，agent 讀到的就不是規範了。
VENDOR_ENTRIES = ["AGENTS.md", "GEMINI.md"]

# 附錄順序：(reference 檔, 附錄編號中文)
APPENDICES = [
    ("official-letter.md", "一"),
    ("terminology-tables.md", "二"),
    ("gov-documents.md", "三"),
    ("legal-documents.md", "四"),
    ("civil-petition.md", "五"),
]

FRONTMATTER = """---
name: tw-formal-writing-standalone
description: >
  台灣正式文件撰寫助手（獨立單檔版本，適用於 ChatGPT / Gemini）— 涵蓋政府公文、政府非公文文件、法律文件、人民對政府文書四類中文正式文件的撰寫（不含學術論文、商業文書、私人書信等，見下方排除清單）。
  根據使用者意圖自動判斷文件類別，依照對應的撰寫規範與格式指引產出文件。
  本檔案為完整獨立版本，所有規範與參考資料皆內含於此單一檔案中。

  觸發此 skill 的情境：
  - 政府公文：簽、函、書函、公告、令、呈、咨、箋函、便簽、行文、發文、簽辦、擬稿、陳核、簽稿併陳、以稿代簽、先簽後稿、上行文、下行文、平行文
  - 政府非公文文件：會議紀錄、開會通知單、新聞稿、聲明稿、施政報告、出國報告、施政計畫書、業務計畫書、裁處書、訴願決定書、聘函、獎狀、證書
  - 法律文件：存證信函、律師函、合約書、備忘錄(MOU)、保密協議(NDA)、聲明書、切結書、委託書、授權書
  - 人民對政府文書：陳情書、申請書、訴願書、異議書、申覆書
  - 描述需要撰寫正式文件的情境（如「幫我寫一封給教育部的公文」「我要寄存證信函」「幫我寫陳情書」）
  - 詢問任何正式文件的格式或用語規範
  - 公務員考試或受訓的公文練習題

  不應觸發的情境：
  - 商業 email、求職信、履歷
  - 學術論文、研究計畫書
  - 商業計畫書、簡報
  - 私人書信、感謝卡
  - 翻譯任務
  - 純粹的文章潤飾或改寫
metadata:
  version: {version}
  last_updated: {last_updated}
  status: active
---

"""

WARNING = "<!-- 本檔由 scripts/build.py 從 references/ 自動生成，請勿手動編輯。改規範請改 references/ 後重新 build。 -->\n\n"

# references 內的跨檔指涉 → STANDALONE 內的附錄指涉(讓單檔讀起來自然)
CROSS_REF_FIXES = [
    ("`official-letter.md`", "附錄一（政府公文撰寫規範）"),
    ("更完整的用語對照表請參閱 `references/terminology-tables.md`。", "更完整的用語對照表請參閱附錄二（公文用語詳細對照表）。"),
]


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def get_skill_meta() -> tuple[str, str]:
    """從 SKILL.md frontmatter 取 version / last_updated。"""
    text = read(ROOT / "SKILL.md")
    version = re.search(r"^\s*version:\s*(\S+)", text, re.M)
    updated = re.search(r"^\s*last_updated:\s*(\S+)", text, re.M)
    if not version or not updated:
        sys.exit("ERROR: SKILL.md frontmatter 缺 version / last_updated")
    return version.group(1), updated.group(1)


def build() -> str:
    version, updated = get_skill_meta()
    parts = [FRONTMATTER.format(version=version, last_updated=updated), WARNING]

    header = read(REF / "_header.md").rstrip() + "\n"
    parts.append(header)

    for fname, num in APPENDICES:
        body = read(REF / fname).rstrip()
        # 第一個 H1「# xxx規範」→「# 附錄N：xxx規範」
        body = re.sub(r"^# (.+)$", rf"# 附錄{num}：\1", body, count=1, flags=re.M)
        # 跨檔指涉 → 附錄指涉
        for src, dst in CROSS_REF_FIXES:
            body = body.replace(src, dst)
        parts.append("\n---\n\n" + body + "\n")

    return "\n".join(parts).rstrip() + "\n"


def plugin_skill_contents() -> dict[str, str]:
    """plugin skill 目錄該有的內容：{目錄內相對路徑: 檔案內容}。

    SKILL.md 執行期讀 `references/*.md`、並指引使用者看 `examples/`；plugin 載入時
    這些相對路徑是相對於 skill 目錄解析，所以兩個目錄都要在。
    """
    files = {"SKILL.md": read(ROOT / "SKILL.md")}
    for src_dir in (REF, EXAMPLES):
        for f in sorted(src_dir.glob("*.md")):
            files[f"{src_dir.name}/{f.name}"] = read(f)
    return files


def sync_plugin_skill(check: bool) -> bool:
    """把 SSOT 鏡射進 skills/tw-formal-writing/。check 模式只比對，回傳是否一致。"""
    want = plugin_skill_contents()

    if check:
        have = {
            p.relative_to(PLUGIN_SKILL).as_posix(): read(p)
            for p in PLUGIN_SKILL.rglob("*") if p.is_file()
        } if PLUGIN_SKILL.is_dir() else {}
        if have != want:
            print("FAIL: skills/tw-formal-writing/ 與 SKILL.md / references/ / examples/ 不一致。"
                  "請跑 python3 scripts/build.py 重新生成。")
            return False
        print(f"OK: skills/tw-formal-writing/ 與 source 一致（{len(want)} 檔）")
        return True

    # 整個重建：舊檔可能是 symlink（v1.2.2 的做法），直接寫入會穿透寫回 SSOT
    if PLUGIN_SKILL.is_symlink():
        PLUGIN_SKILL.unlink()
    elif PLUGIN_SKILL.exists():
        shutil.rmtree(PLUGIN_SKILL)
    for rel, text in want.items():
        dst = PLUGIN_SKILL / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
    print(f"已生成 skills/tw-formal-writing/（{len(want)} 檔）")
    return True


def sync_vendor_entries(standalone: str, check: bool) -> bool:
    """把 STANDALONE.md 的內容鏡射到 AGENTS.md / GEMINI.md。check 模式只比對。"""
    stale = [f for f in VENDOR_ENTRIES
             if not (ROOT / f).is_file() or read(ROOT / f) != standalone]

    if check:
        if stale:
            print(f"FAIL: {' / '.join(stale)} 與 STANDALONE.md 不一致。"
                  "請跑 python3 scripts/build.py 重新生成。")
            return False
        print(f"OK: {' / '.join(VENDOR_ENTRIES)} 與 STANDALONE.md 一致")
        return True

    for f in VENDOR_ENTRIES:
        p = ROOT / f
        # 舊版是 symlink 指向 STANDALONE.md，直接寫入會穿透覆蓋目標
        if p.is_symlink():
            p.unlink()
        p.write_text(standalone, encoding="utf-8")
    print(f"已生成 {' / '.join(VENDOR_ENTRIES)}")
    return True


def main() -> None:
    result = build()
    if "--check" in sys.argv:
        current = read(OUT) if OUT.exists() else ""
        ok = True
        if current != result:
            print("FAIL: STANDALONE.md 與 references/ 不一致。請跑 python3 scripts/build.py 重新生成。")
            ok = False
        else:
            print("OK: STANDALONE.md 與 source 一致")
        if not sync_plugin_skill(check=True):
            ok = False
        if not sync_vendor_entries(result, check=True):
            ok = False
        if not ok:
            sys.exit(1)
    else:
        OUT.write_text(result, encoding="utf-8")
        print(f"已生成 STANDALONE.md（{len(result.splitlines())} 行）")
        sync_plugin_skill(check=False)
        sync_vendor_entries(result, check=False)


if __name__ == "__main__":
    main()
