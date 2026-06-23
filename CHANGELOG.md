# Changelog

本檔案記錄台灣正式文件撰寫 AI Skill 的版本歷史。

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
