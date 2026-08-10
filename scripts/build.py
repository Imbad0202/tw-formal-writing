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

# references 內的跨檔指涉 → STANDALONE 內的附錄指涉(讓單檔讀起來自然)。
# 用 regex 涵蓋 `xxx.md` 與 `references/xxx.md` 兩種寫法：早期是逐句字面比對，
# 新增的第二種句型就漏改、把死連結留在單檔版裡(v1.3.0 起殘留於 STANDALONE 780 行)。
# 前後各吃掉一個可能的空格：原文的空格是給行內程式碼留的間隔，換成中文詞之後
# 留著就變成中文字之間的贅空格。
CROSS_REF_RE = re.compile(
    r" ?`(?:references/)?(" + "|".join(re.escape(f) for f, _ in APPENDICES) + r")` ?"
)
APPENDIX_NUM = {fname: num for fname, num in APPENDICES}


def within_repo(p: Path) -> bool:
    """p 解析後是否仍落在 repo 內（不存在或解析失敗都算不在）。

    用 resolve() 而不是 is_symlink()：後者只看路徑末端，`references/` 這個「目錄」
    被換成指向 repo 外的 symlink 時，底下每個 .md 的 is_symlink() 都是 False，
    檢查末端完全擋不住。resolve() 會把中間每一段都攤開，兩種情況一起涵蓋。
    """
    try:
        return ROOT in p.resolve(strict=True).parents
    except OSError:
        return False


def read(p: Path) -> str:
    """讀 source 檔，但拒絕解析到 repo 外的路徑。

    擋在最底層是刻意的：規範內容會被鏡射進 git 追蹤的 skills/、組進 STANDALONE.md
    (以及 AGENTS.md / GEMINI.md)、打進公開 Release 的 zip。任何一條讀取路徑漏掉檢查，
    一個指向 repo 外的 .md（或一個被換掉的 references/ 目錄）就能把本機檔案內容
    推上這個 public repo。
    也不「跳過就算了」——那會讓整類規範默默消失而所有 gate 仍綠(v1.4.1 初版的錯)。
    """
    if not within_repo(p):
        sys.exit(f"ERROR: {p} 解析後不在 repo 內。source 檔不得為 symlink、"
                 "也不得指向 repo 外，請改為實體檔。")
    return p.read_text(encoding="utf-8")


def cross_ref_fix(text: str) -> str:
    """把跨檔指涉改寫成附錄指涉（單檔版沒有 references/，留著就是死連結）。"""
    return CROSS_REF_RE.sub(lambda m: f"附錄{APPENDIX_NUM[m.group(1)]}", text)


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

    # 頭部也要跑跨檔指涉改寫：只改附錄本體的話，寫在 _header.md 裡的跨檔指涉
    # 會被下面的收尾斷言擋下來（維護者寫一句自然的指涉就 build 不過）。
    header = cross_ref_fix(read(REF / "_header.md").rstrip()) + "\n"
    parts.append(header)

    for fname, num in APPENDICES:
        body = read(REF / fname).rstrip()
        # 第一個 H1「# xxx規範」→「# 附錄N：xxx規範」
        body = re.sub(r"^# (.+)$", rf"# 附錄{num}：\1", body, count=1, flags=re.M)
        # 跨檔指涉 → 附錄指涉
        body = cross_ref_fix(body)
        parts.append("\n---\n\n" + body + "\n")

    result = "\n".join(parts).rstrip() + "\n"

    # 收尾斷言：單檔版不該再有指向 references/ 的路徑，那對單檔使用者是死連結。
    # WARNING 那行是 build 自己的註解、本來就會提到 references/，整行比對後排除
    #（不能用 `line not in WARNING` 這種子字串測試——任何剛好是 WARNING 子字串的
    # 內容行都會被誤放行）。
    warning_lines = set(WARNING.splitlines())
    leftovers = [
        line for line in result.splitlines()
        if "references/" in line and line not in warning_lines
    ]
    if leftovers:
        sys.exit("ERROR: 生成內容仍殘留指向 references/ 的死連結：\n  "
                 + "\n  ".join(leftovers))

    return result


def assert_within_repo(path: Path) -> None:
    """確認 path 解析後仍落在 repo 內的預期位置，否則中止。

    走的是 parent 的 resolve()：path 自己可能還不存在（尚未建立），但它上層若被
    換成指向 repo 外的 symlink，parent 解析出來就會跑出 ROOT。
    """
    parent = path.parent.resolve()
    root = ROOT.resolve()
    if parent != root and root not in parent.parents:
        sys.exit(f"ERROR: {path} 的上層解析到 repo 外（{parent}），拒絕寫入或刪除。"
                 f"請檢查 {path.parent.name}/ 是否被換成 symlink。")


def plugin_skill_contents() -> dict[str, str]:
    """plugin skill 目錄該有的內容：{目錄內相對路徑: 檔案內容}。

    SKILL.md 執行期讀 `references/*.md`、並指引使用者看 `examples/`；plugin 載入時
    這些相對路徑是相對於 skill 目錄解析，所以兩個目錄都要在。
    """
    files = {"SKILL.md": read(ROOT / "SKILL.md")}
    for src_dir in (REF, EXAMPLES):
        for f in sorted(src_dir.glob("*.md")):
            files[f"{src_dir.name}/{f.name}"] = read(f)  # read() 擋 symlink
    return files


def sync_plugin_skill(check: bool) -> bool:
    """把 SSOT 鏡射進 skills/tw-formal-writing/。check 模式只比對，回傳是否一致。"""
    want = plugin_skill_contents()

    if check:
        # 先比檔名集合，再只讀「該有的檔」。不要無差別讀取目錄下每個檔——
        # 一個 .DS_Store 之類的二進位雜檔就會讓 read() 丟 UnicodeDecodeError，
        # CI 直接 traceback 死掉、且訊息完全指不到問題。
        # 忽略點檔（.DS_Store 之類 macOS 在 Finder 開資料夾就會生的雜檔）：它們不是
        # 鏡射內容的一部分，拿它們去 FAIL 只會讓本機檢查無故變紅、且無法自癒。
        have_names = {
            rel for p in PLUGIN_SKILL.rglob("*") if p.is_file()
            for rel in [p.relative_to(PLUGIN_SKILL).as_posix()]
            if not any(part.startswith(".") for part in Path(rel).parts)
        } if PLUGIN_SKILL.is_dir() else set()
        if have_names != set(want):
            extra = sorted(have_names - set(want))
            missing = sorted(set(want) - have_names)
            detail = "；".join(filter(None, [
                f"多出 {'、'.join(extra)}" if extra else "",
                f"缺少 {'、'.join(missing)}" if missing else "",
            ]))
            print(f"FAIL: skills/tw-formal-writing/ 檔案清單不符（{detail}）。"
                  "請跑 python3 scripts/build.py 重新生成。")
            return False
        stale = [rel for rel, text in want.items() if read(PLUGIN_SKILL / rel) != text]
        if stale:
            print(f"FAIL: skills/tw-formal-writing/ 內容過期（{'、'.join(stale)}）。"
                  "請跑 python3 scripts/build.py 重新生成。")
            return False
        print(f"OK: skills/tw-formal-writing/ 與 source 一致（{len(want)} 檔）")
        return True

    # 確認要動的是 repo 內那個目錄，再刪、再寫。檢查必須在「刪除與寫入」兩者之前：
    # 只擋刪除的話，skills/ 指向 repo 外、而外面還沒有 tw-formal-writing/ 時，
    # 兩個分支都不進，下面的 mkdir(parents=True) 會直接在 repo 外建目錄寫 11 個檔。
    # 只驗末端是不是 symlink 也不夠——上層 skills/ 被換掉時末端不是 symlink。
    assert_within_repo(PLUGIN_SKILL)

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
        assert_within_repo(p)
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
