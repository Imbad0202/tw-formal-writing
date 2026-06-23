#!/usr/bin/env python3
"""從 source 檔組裝 STANDALONE.md。

Single source of truth:
- frontmatter version 取自 SKILL.md
- 頭部(類別判斷/把關/共通原則/互動流程)= references/_header.md
- 五個附錄 = references/*.md(各自降級成「附錄N」標題)

STANDALONE.md 是生成產物，不應手動編輯。改規範請改 references/。
用法: python3 scripts/build.py        # 寫出 STANDALONE.md
      python3 scripts/build.py --check # 只檢查是否與現檔一致(CI 用)，不一致則 exit 1
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REF = ROOT / "references"
OUT = ROOT / "STANDALONE.md"

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
  台灣正式文件撰寫助手（獨立單檔版本，適用於 ChatGPT / Gemini）— 涵蓋政府公文、政府非公文文件、法律文件、人民對政府文書等所有中文正式文件的撰寫。
  根據使用者意圖自動判斷文件類別，依照對應的撰寫規範與格式指引產出文件。
  本檔案為完整獨立版本，所有規範與參考資料皆內含於此單一檔案中。

  觸發此 skill 的情境：
  - 政府公文：簽、函、書函、公告、令、呈、咨、箋函、便簽、行文、發文、簽辦、擬稿、陳核、簽稿併陳、以稿代簽、先簽後稿、上行文、下行文、平行文
  - 政府非公文文件：會議紀錄、開會通知單、新聞稿、聲明稿、施政報告、出國報告、計畫書、裁處書、訴願決定書、聘函、獎狀、證書
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


def main() -> None:
    result = build()
    if "--check" in sys.argv:
        current = read(OUT) if OUT.exists() else ""
        if current != result:
            print("FAIL: STANDALONE.md 與 references/ 不一致。請跑 python3 scripts/build.py 重新生成。")
            sys.exit(1)
        print("OK: STANDALONE.md 與 source 一致")
    else:
        OUT.write_text(result, encoding="utf-8")
        print(f"已生成 STANDALONE.md（{len(result.splitlines())} 行）")


if __name__ == "__main__":
    main()
