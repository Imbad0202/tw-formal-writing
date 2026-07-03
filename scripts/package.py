#!/usr/bin/env python3
"""打包 skill.zip（供 claude.ai / cowork 上傳載入）。

zip 內容 = 頂層資料夾 tw-formal-writing/ 內含 SKILL.md + references/ 全部檔案，
符合多檔案 skill 包結構（執行期 SKILL.md 動態讀 references/*.md）。
版本號取自 SKILL.md frontmatter（與 build.py 同源，單一真實來源）。

打包前會先確認 STANDALONE.md 是 references/ 的最新 build 產物（呼叫 build.py --check），
避免把過期內容打進發布包。

用純 Python zipfile，不依賴系統 zip 指令（避免 shell 手動打包時的斷行 / 引號問題）。

用法: python3 scripts/package.py            # 寫出 dist/tw-formal-writing-skill-v{version}.zip
      python3 scripts/package.py --check    # 只驗證該裝的檔都在、STANDALONE 為最新，不寫檔（CI / 發版前用）
      python3 scripts/package.py --release  # 打包後自動建 GitHub Release（掛在 v{version} tag、附 zip、notes 取 CHANGELOG 對應段）
"""
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # 複用 SKILL.md frontmatter 的 version 解析（單一真實來源）

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
REF = ROOT / "references"
EXAMPLES = ROOT / "examples"
LICENSE = ROOT / "LICENSE"
DIST = ROOT / "dist"
CHANGELOG = ROOT / "CHANGELOG.md"

# zip 內的頂層資料夾名（claude.ai / cowork 以此為 skill 名載入）
PKG_NAME = "tw-formal-writing"


def get_version() -> str:
    """從 SKILL.md frontmatter 取 version（複用 build.get_skill_meta，避免解析邏輯分岔）。"""
    version, _ = build.get_skill_meta()
    return version


def collect_files() -> tuple[list[Path], list[str]]:
    """要打包進 skill 包的檔，回傳 (檔案清單, 缺檔訊息)。

    純函式：不 sys.exit，讓 CLI（main）與 CI 檢查（check_consistency.check_package_manifest）
    共用同一份清單邏輯、各自決定失敗怎麼處理。缺檔訊息非空即代表打包內容會不完整。

    多檔案 skill 包（claude.ai / cowork 上傳用）內容：
    - SKILL.md：進入點（執行期動態讀 references/、並指引使用者看 examples/）
    - references/*.md：四類文件的撰寫規範（SKILL.md 依判斷結果讀取）
    - examples/*.md：SKILL.md 內文「更多範例請見 examples/ 目錄」指向的示範文件
    - LICENSE：對外散布附授權條款（MIT）

    不含 STANDALONE.md / LITE.md：那是「單檔上傳」管道（ChatGPT / Gemini / Claude
    Project Knowledge）的產物，多檔案 skill 包內為冗餘。README / CITATIONS 屬 repo
    治理檔，skill 執行期不讀，亦不入包。

    references/ 與 examples/ 用 glob 自動抓，新增檔不漏。
    """
    errors: list[str] = []
    if not SKILL.exists():
        errors.append("找不到 SKILL.md")
    refs = sorted(REF.glob("*.md"))
    if not refs:
        errors.append("references/ 下沒有任何 .md，打包內容會不完整")
    examples = sorted(EXAMPLES.glob("*.md"))
    if not examples:
        errors.append("examples/ 下沒有任何 .md，但 SKILL.md 指向該目錄，打包內容會不完整")
    if not LICENSE.exists():
        errors.append("找不到 LICENSE，對外散布的 skill 包應附授權條款")
    files = [SKILL, *refs, *examples, LICENSE] if not errors else []
    return files, errors


def check_standalone_built() -> None:
    """確認 STANDALONE.md 是 references/ 的最新 build 產物，否則發布包可能含過期內容。"""
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build.py"), "--check"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        sys.exit("ERROR: STANDALONE.md 不是 references/ 的最新 build 產物。請先跑 python3 scripts/build.py")


def arcname(f: Path) -> str:
    """zip 內路徑：頂層資料夾 + 相對 ROOT 的路徑（SKILL.md 或 references/xxx.md）。"""
    return f"{PKG_NAME}/{f.relative_to(ROOT).as_posix()}"


def changelog_notes(version: str) -> str:
    """擷取 CHANGELOG 中 [version] 段（到下一個 ## 為止）作為 release notes。查不到則回退為版本標題。"""
    if not CHANGELOG.exists():
        return f"v{version}"
    text = CHANGELOG.read_text(encoding="utf-8")
    # 從 ## [version] 抓到下一個 ## （或檔尾）
    m = re.search(rf"^## \[{re.escape(version)}\].*?(?=^## |\Z)", text, re.M | re.S)
    return m.group(0).strip() if m else f"v{version}"


def create_release(version: str, zip_path: Path) -> None:
    """建 GitHub Release：掛在 v{version} tag、附 zip、notes 取 CHANGELOG 對應段。

    對外不可逆動作，先做前置檢查；同名 release 已存在則不覆蓋、報錯停。
    """
    if not shutil.which("gh"):
        sys.exit("ERROR: 找不到 gh CLI，無法建 release。請安裝 GitHub CLI 或改用手動 gh release create。")

    tag = f"v{version}"
    # tag 必須已存在（release 掛在 tag 上；本腳本不代建 tag，發版流程另行 tag）
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--verify", f"refs/tags/{tag}"],
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ERROR: tag {tag} 不存在。請先 git tag {tag} 並 push，再建 release。")

    # 同名 release 已存在 → 不覆蓋，避免誤刪手動建好的版本
    r = subprocess.run(["gh", "release", "view", tag, "-R", "Imbad0202/tw-formal-writing"],
                       capture_output=True, text=True, cwd=str(ROOT))
    if r.returncode == 0:
        sys.exit(f"ERROR: release {tag} 已存在，不覆蓋。要更新請手動處理，或先刪除既有 release。")

    notes = changelog_notes(version)
    r = subprocess.run(
        ["gh", "release", "create", tag, str(zip_path),
         "--title", tag, "--notes", notes],
        cwd=str(ROOT),
    )
    if r.returncode != 0:
        sys.exit(f"ERROR: gh release create 失敗（exit {r.returncode}）")
    print(f"已建 GitHub Release {tag}（附 {zip_path.name}）")


def main() -> None:
    check_standalone_built()
    version = get_version()
    files, errors = collect_files()
    if errors:
        sys.exit("ERROR: " + "；".join(errors))
    out = DIST / f"{PKG_NAME}-skill-v{version}.zip"

    if "--check" in sys.argv:
        # 只驗證：SKILL.md + 至少一個 reference 在，STANDALONE 已於上面驗過
        names = [arcname(f) for f in files]
        print(f"OK: 打包清單就緒（{len(files)} 檔，version {version}）")
        for n in names:
            print(f"  - {n}")
        print(f"目標: {out.relative_to(ROOT)}（--check 未寫檔）")
        return

    DIST.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, arcname(f))
    print(f"已打包 {out.relative_to(ROOT)}（{len(files)} 檔，version {version}）")

    if "--release" in sys.argv:
        create_release(version, out)


if __name__ == "__main__":
    main()
