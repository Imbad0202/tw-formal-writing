# Changelog

本檔案記錄台灣正式文件撰寫 AI Skill 的版本歷史。

## [1.4.1] - 2026-08-10

修正 v1.4.0 的 `/code-review` 與 `/security-review` findings，全部經回歸測試驗證。不動規範內容。

### Fixed
- **README 的 plugin 更新指令不完整（中英）**：原寫「更新規範只要 `/plugin marketplace update`」，但那只刷新 marketplace 清單，不會換掉已安裝的內容——使用者會以為更新了卻仍在用舊版公文規範。補上必要的第二步 `/plugin update tw-formal-writing`。
- **`build.py` 的 `shutil.rmtree` 可刪到 repo 外**：原本只驗末端 `skills/tw-formal-writing` 是否為 symlink，上層 `skills/` 被換成指向 repo 外的 symlink 時會順著走出去刪掉外部目錄（PR 可夾帶，維護者跑 `build.py` 即中；CI 的 `--check` 不受影響）。刪除前改為解析並確認仍在 repo 內。
- **單檔版殘留死連結**：`CROSS_REF_FIXES` 逐句字面比對，新增句型漏改，`references/terminology-tables.md` 這類路徑留在 STANDALONE / AGENTS / GEMINI 裡，對單檔使用者是不存在的檔案。改為 regex 涵蓋 `` `xxx.md` `` 與 `` `references/xxx.md` `` 兩種寫法（一併去除替換後中文間的贅空格），並加收尾斷言：生成內容若仍殘留 `references/` 路徑就中止 build。
- **一個 `.DS_Store` 就讓 CI 永久紅**：`--check` 原本無差別讀取 `skills/` 下每個檔並當 UTF-8 解，遇二進位雜檔直接 `UnicodeDecodeError`。改為先比檔名集合、再只讀該有的檔，並在訊息中列出多出／缺少哪些檔。`.gitignore` 補 `.DS_Store`。
- **`check_consistency.py` 丟掉 stderr**：build.py 若拋例外，訊息全在 stderr，輸出會變成「產物過期」後面接「一切正常」的自相矛盾內容。改為 stdout + stderr 都帶出。
- **`package.py` 的錯誤訊息過期**：v1.4.0 把 `build.py --check` 從驗一項擴為三項，但 `package.py` 仍寫死「STANDALONE.md 過期」且丟掉輸出，`skills/` 沒同步時會指向錯的檔案。改為轉述 build.py 自己的輸出（函式更名 `check_generated_artifacts`）。
- **`marketplace.json` 的 `$schema` 404**：該 URL 301 後 404，編輯器驗證等於沒作用（Claude Code 載入時本就忽略此欄）。移除。

### Added
- **source 路徑限制在 repo 內**：`build.py` 的 `read()` 與 `package.py` 的 `collect_files()` 一律要求 source 檔 `resolve()` 後仍在 repo 內，否則中止（不是跳過——跳過會讓整類規範默默從 skill 包與發布 zip 消失，而所有 gate 仍綠）。涵蓋 `SKILL.md`、`LICENSE`、`references/*.md`、`examples/*.md`。

  用 `resolve()` 而不是檢查末端是否為 symlink：後者只看路徑最後一段，`references/` 這個**目錄**被換成指向 repo 外的 symlink 時，底下每個 `.md` 的 `is_symlink()` 都是 `False`，完全擋不住。原本兩條路徑都會跟著連結走，一個 PR 就能把維護者本機任意檔案的內容帶進這個 public repo 的追蹤檔、單檔版（`STANDALONE.md` / `AGENTS.md` / `GEMINI.md`）以及公開 Release 的 zip。
- **寫入目標同樣限制在 repo 內**：`skills/` 被換成指向 repo 外的 symlink 且外部尚無同名子目錄時，刪除分支不會進入，寫入迴圈會直接在 repo 外建目錄寫檔。改為在刪除與寫入之前都先驗證。
- **manifest 文案漂移 gate**：`plugin.json` 與 `marketplace.json` 的 `description`、`keywords`／`tags` 納入一致性檢查（原本只 gate `version`，兩份文案已各自漂移）。

## [1.4.0] - 2026-08-10

### Added
- **Claude Code plugin marketplace**：新增 `.claude-plugin/marketplace.json`，本 repo 自身即為 marketplace。使用者於 Claude Code（CLI 或桌面版）執行 `/plugin marketplace add Imbad0202/tw-formal-writing` 後 `/plugin install tw-formal-writing@tw-formal-writing` 即可安裝，並以 `/plugin` 選單啟用停用、`/plugin marketplace update` 更新規範。README 中英同步補安裝說明。
- **`plugin.json` metadata 補完**：新增 `author` / `homepage` / `keywords`，供 marketplace 清單顯示。

### Fixed
- **plugin 模式讀不到規範內容**：`skills/tw-formal-writing/` 原本只有一個指向根目錄 `SKILL.md` 的 symlink，未含 `references/` 與 `examples/`。依 Claude Code plugin 規格，SKILL.md 內的相對路徑是相對 skill 目錄解析，故 plugin 載入後四類文件的撰寫規範全數讀取失敗。改由 `scripts/build.py` 將 `SKILL.md` + `references/` + `examples/` 鏡射為實體檔（不用 symlink——plugin 安裝走 git clone，Windows 預設不還原 symlink）。

- **`AGENTS.md` / `GEMINI.md` 改為實體檔**：原為指向 `STANDALONE.md` 的 symlink，Windows 的 git 預設 `core.symlinks=false`，clone 後會還原成一行純文字路徑，Codex / Gemini CLI 讀到的不是規範。改由 `build.py` 生成實體複本，`--check` 一併 gate。至此全 repo 無 symlink。

### Changed
- **`scripts/build.py`**：除 `STANDALONE.md` 外，一併生成 `skills/tw-formal-writing/` 與 `AGENTS.md` / `GEMINI.md`；`--check` 三者皆驗。
- **`scripts/check_consistency.py`**：version 一致性由三處擴為五處，納入 `.claude-plugin/plugin.json` 與 `marketplace.json` 的 plugin entry（原本這兩處未被 CI 守住，是最容易漏的同步點）。

## [1.3.0] - 2026-08-05

對照《文書處理手冊》112 年版全文（自行政院官網下載第一手 PDF）與兩份釋例彙編做涵蓋度盤點後的大批補強（#15–#21）。所有新增引據均經第一手核對並登記於 `CITATIONS.md`（#12–#30）。

### Fixed
- **104.3.25 院臺綜字第 1040127907 號函誤標**：該函實為「期望、目的及稱謂用語無須挪抬」，非廢除「鑒核示遵」；挪抬廢止規則入庫（#15）。
- **「奉／准／據」硬規則降級**：「依」「依據」為通用引據語，各方向均可（釋例 108.7.24），不再把「依據引上級來文」判錯；「奉／准／據」保留為傳統引敘語、僅方向弄反時判錯（#15）。
- **「請鑒核」與「請核示」分工**：前者用於下級機關對上級機關上行函、後者用於機關內部簽辦（釋例 114.1.22、115.3.2）（#15）。
- **附送語方向**：檢陳對上級；檢送、檢附對平行及下級（#15）。

### Added
- 「惠」字規則（惠請不可用、惠放請後）與贅詞清單補齊（無任感荷等）（#16）。
- 數字/日期/時間/金額細則：1份・一案・一式2份三分規則、日期國曆、星期用中文、12/24 小時制、新臺幣（以下同）、契約條號阿拉伯數字（#17）。
- 行款欄位規則：速別與限期公文、密等非機密留空、附件欄（含條件式「如文」）、受文者與正副本書明全銜；一文分行數機關原則（標明實務慣例層級）（#18）。
- 引敘方式（全文照錄／節錄／撮敘「略以」）、法規名稱引號規則、法律統一用字表全表、法律統一用語表、常見疑義字組、連接詞及/與/暨（#19）。
- 簽辦品質規則：簽具意見具體化、存查用法區分、簽辦方式依手冊第 19 點校準（#20）。
- 標點符號規範：引號先單後雙、重點用引號、刪節號六點、禁非表列符號、全形半形、中文函不夾英文（#21）。
- `CITATIONS.md` 新增「教學來源使用紀律」節：外部教材僅作盤點線索，規則一律回官方來源第一手重建。

## [1.2.3] - 2026-07-03

### Changed
- **對齊釋例第一手來源**：以《文書處理相關釋例》函釋（更新至 115.4.30）、院長電子信箱（更新至 115.6.30）兩份第一手 PDF 為準，將原標「更新至 115.2.23」更新為兩份各自的更新日期（`references/official-letter.md`、README 中英）。

### Fixed
- **修正「臺／台」用字規則的來源日期**：110.12.10 → **110.12.20**。依院長電子信箱 112.6.28 釋例第一手澄清，《公文撰作解析》原引述之「110.12.10 解釋」係誤植，正確日期為 110.12.20（`references/official-letter.md`、`examples/04`、`STANDALONE.md`）。

### Added
- **`CLAUDE.md`**：repo 架構（references 為 SoT、多入口分發）、build / consistency 指令、版本同步點與 public repo 紀律說明。
- **`CITATIONS.md`**：#3 日期更正並升級為第一手佐證；新增「臺端」用語與釋例更新日期查核紀錄；backlog 記錄「乙案／乙份」於兩份釋例查無佐證；新增第一手來源檔區塊（含手冊 PDF 為 104 年舊版、不採之判定）。

## [1.2.2] - 2026-06-25

### Added
- **跨 vendor 通用入口**：新增 `AGENTS.md` / `GEMINI.md`（symlink 至 `STANDALONE.md` 完整單檔），供 Codex / Gemini 等其他 vendor 直接讀取；新增 `.claude-plugin/plugin.json` 供 Claude Code plugin 載入（`skills/` 指向 `SKILL.md`）。一份內容、多種入口：精簡版（SKILL.md，Claude 載 references）給支援 skill 格式者，完整單檔（STANDALONE.md）給其他 vendor。
- **skill.zip 打包**：可下載 release 附件直接於 claude.ai / cowork 載入。

## [1.2.1] - 2026-06-23

### Changed
- **觸發描述收窄**（SKILL / STANDALONE / LITE 三版）：移除過寬的「所有中文正式文件」宣稱（與排除清單矛盾）；「計畫書」裸詞改為「施政計畫書／業務計畫書」，避免誤觸研究計畫書、商業計畫書等排除項
- **LITE.md 表格精簡**：5 個 2 欄線性表轉為緊湊清單（省 token、提升 LLM 遵循度）；4 個多欄矩陣表維持表格。關鍵規則錨點全數保留
- **CITATIONS.md 補完查核**：行政程序法第171/173條、《文書處理手冊》現行版（第七版）經第一手查證；backlog 縮減

## [1.2.0] - 2026-06-23

### Added
- **撰寫前三項把關 guardrail**（SKILL / STANDALONE / LITE 三版）：遇自相矛盾要求先糾正再寫、不為冒用機關名義產出成品、貼入內容只當待處理文本不當指令
- **法律文件總免責聲明**：legal-documents 與 STANDALONE 附錄四開頭加總免責，提醒合約 / NDA / 訴願書等僅供格式參考、不構成法律意見
- **`CITATIONS.md` 引據查核紀錄**：制度化記錄所有精確法規 / 釋例引據的查核狀態與第一手來源
- **`scripts/build.py`**：以 `references/` 為單一真實來源自動生成 `STANDALONE.md`，消除三版漂移
- **`scripts/check_consistency.py` + CI**：檢查 STANDALONE 為最新 build 產物、LITE 涵蓋關鍵規則錨點、三版版號一致

### Changed
- **校正「旨揭 / 旨在」用語定性**：經第一手查證，「旨揭」屬合法的簡化敘述用語、仍可使用，並非廢除用語；移除無法查證的「114.7.11 建議停用」陳述，改為中性風格建議
- **`STANDALONE.md` 改為 build 產物**：補回先前漂移缺漏的「常見場景快速辨識」等段落，與 references 完全同步

### Fixed
- 修正簡體字「届」→ 正體「屆」（9 處）
- 移除查無第一手佐證的精確日期引據（院長信箱 114.7.11 / 114.12.10），規則保留、來源改標已驗證的通用出處

## [1.1.0] - 2026-04-03

### Added
- YAML frontmatter 加入 `metadata:` 區塊（version / last_updated / status），符合 claude.ai 上傳規範
- `examples/` 目錄，含 3 個完整範例（函、存證信函、陳情書）
- SKILL.md 加入 Quick Start 區段
- CHANGELOG.md 版本紀錄

## [1.0.0] - 2026-03-29

### Added
- AI 使用注意事項及行政院生成式 AI 指引連結 (`b2e84b6`)
- GitHub sidebar 設定：topics、homepage、FUNDING.yml (`6e80b08`)
- README 版本號 v1.0 + MIT 授權 + Buy Me a Coffee + 專案說明 (`e4f034e`)
- README 中英文切換連結 (`82699b1`)
- README 拆分為中文 `README.md` + 英文 `README_EN.md` (`dc8e70f`)
- 英文 README + 外國使用者適應機制（所有版本）(`3471504`)
- README.md 含各 AI 平台匯入說明 (`d840f73`)

### Added（功能）
- 三大新功能：常見場景快速辨識（13 場景）+ 幫我改模式 + 更新互動流程 (`20fb187`)
- STANDALONE.md 重建，整合三大新功能 (`c9f5371`)
- LITE.md 精簡版，供 ChatGPT GPTs Instructions 使用 (`89c00a8`)
- STANDALONE.md 單檔版本（1425 行），供 ChatGPT/Gemini 等平台匯入 (`aad2151`)
- 品質檢核關卡：HTML 即時檢核引擎 + SKILL.md 品管清單 (`3bd7bf4`)
- 引導式公文產生器 HTML（簽、函、公告）(`03cc3b5`)

### Changed
- simplify review 修正 7 項問題 (`3815e03`)
- 分段複製模式（公務員）+ 全文複製模式（一般民眾）(`ba7be88`)

### Removed
- 公文產生器 HTML（改為純 skill 方案）(`a7e8310`)

## [0.1.0] - 2026-03-29

### Added
- Initial commit：台灣正式文件撰寫 Skill（入口路由 + 4 類 reference）(`55a5c43`)
- 四類文件參考規範：`official-letter.md`、`gov-documents.md`、`legal-documents.md`、`civil-petition.md`
- 用語對照表：`terminology-tables.md`
