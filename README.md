**[English](README_EN.md)** | 中文

# 台灣正式文件撰寫 AI Skill

[![Version](https://img.shields.io/badge/version-v1.1.0-blue)](https://github.com/Imbad0202/tw-formal-writing/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-Buy%20Me%20a%20Coffee-orange?logo=buy-me-a-coffee)](https://buymeacoffee.com/crucify020v)

## 為什麼公文寫作很重要？

公文不只是形式。一份寫對的公文，能讓案子順利推動；一份寫錯的公文，輕則退件重寫、延誤時效，重則造成法律爭議或機關間的誤解。

**公務員面臨的現實：**
- 新進人員沒受過完整公文訓練，邊寫邊猜、邊被退件邊學
- 引敘語「奉/准/據」、稱謂語「鈞/貴/大」、期望語「請鑒核/請查照」搞不清楚，用錯就是失禮
- 簽辦方式（先簽後稿、簽稿併陳、以稿代簽）選錯，整個流程要重來
- 已廢除的贅詞（為要、為荷、鑒核示遵）還在用，被長官圈起來退回

**一般民眾面臨的現實：**
- 想向政府陳情、申請、訴願，但完全不知道格式怎麼寫
- 需要寄存證信函給房東，但不確定法律用語對不對
- 訴願書有 30 天法定期限，寫錯格式被退件就來不及了

**這個 Skill 解決什麼問題：**
- 匯入你慣用的 AI 工具（ChatGPT、Claude、Gemini），用口語描述情境，AI 就能產出符合《文書處理手冊》及《公文程式條例》規範的正式文件
- 自動選用正確的用語、格式、簽辦方式
- 產出後自動執行品質檢核，攔截常見錯誤
- 已寫好的公文也能貼入請 AI 幫你檢查修改

## 涵蓋範圍

| 類別 | 文件類型 |
|-----|--------|
| 政府公文 | 簽、函、書函、令、呈、咨、公告、箋函、便簽 |
| 政府其他文件 | 會議紀錄、開會通知單、新聞稿、施政報告、聘函、獎狀 |
| 法律文件 | 存證信函、合約書、律師函、備忘錄(MOU)、聲明書、切結書、委託書 |
| 人民對政府 | 陳情書、申請書、訴願書、異議書 |

## 三個版本

| 檔案 | 大小 | 適用場景 |
|-----|-----|--------|
| `LITE.md` | ~2K 中文字 | ChatGPT GPTs Instructions（有字數限制） |
| `STANDALONE.md` | ~26K 字元 | 檔案上傳（完整版，含品質檢核） |
| `SKILL.md` + `references/` | 多檔案 | Claude Code 等支援多檔案的工具 |

## 匯入方式

### ChatGPT GPTs

**方法 A（推薦）：上傳完整版**
1. 前往 [ChatGPT](https://chat.openai.com) → My GPTs → Create a GPT
2. 在 Configure → Knowledge 上傳 `STANDALONE.md`
3. Instructions 欄位貼入：
   ```
   你是台灣正式文件撰寫專家。請依照 Knowledge 中的 STANDALONE.md 規範，
   協助使用者撰寫公文及正式文件。先判斷文件類別，再依對應規範撰寫。
   產出後執行品質檢核。
   ```

**方法 B：直接貼入精簡版**
1. 前往 My GPTs → Create a GPT
2. 將 `LITE.md` 的全部內容貼入 Instructions 欄位

### ChatGPT Projects

1. 前往 ChatGPT → Projects → 新建或選擇 Project
2. 在 Project 設定中，上傳 `STANDALONE.md` 作為 Project Files
3. 開始對話即可使用

### Claude (claude.ai)

1. 前往 [Claude](https://claude.ai) → Projects → 新建 Project
2. 在 Project Knowledge 上傳 `STANDALONE.md`
3. 在該 Project 中開始對話

### Claude Code

```bash
# 方法 A：全域安裝（所有專案可用）
mkdir -p ~/.claude/skills
git clone https://github.com/Imbad0202/tw-formal-writing.git ~/.claude/skills/tw-formal-writing

# 方法 B：專案內安裝
mkdir -p .claude/skills
git clone https://github.com/Imbad0202/tw-formal-writing.git .claude/skills/tw-formal-writing
```

### Gemini Gems

1. 前往 [Gemini](https://gemini.google.com) → Gems → 新建 Gem
2. 將 `STANDALONE.md` 的全部內容貼入指示欄位（~26K 字元，Gems 上限 ~30K 字元，放得下但接近上限）

## 注意事項

> **依[行政院及所屬機關（構）使用生成式 AI 參考指引](https://www.ey.gov.tw/Page/448DE008087A1971/40c1a925-121d-4b6b-8f40-7e9e1a5401f2)，機密文書應由承辦人親自撰寫，禁止使用生成式 AI 輔助。使用本工具時，請勿輸入涉及機密、未經機關同意公開之資訊，或與案件無關的個資。若屬人民對政府文書，僅提供該程序必要的最小識別與聯絡資訊；除非相關法規、機關表單或案件流程明文要求，避免輸入身分證字號、證件影本等高敏感資料。**

## 使用範例

貼入或上傳完成後，直接跟 AI 說：

- 「我是衛生局的承辦人，需要發函通知各醫療院所下個月要交傳染病統計表」
- 「幫我寫一份簽呈給局長，報告今年度預算執行情形」
- 「我要公告裁罰違規食品業者的結果」
- 「我想寄存證信函催房東退還押金」
- 「幫我寫陳情書向市政府反映噪音問題」

AI 會自動判斷文件類別、確認必要資訊、產出合規文件、執行品質檢核。

## 依據

- 行政院《文書處理手冊》（112 年 6 月 8 日修正）
- 《公文程式條例》
- 國家文官學院《公文撰作解析》（114 年 12 月編印）
- 文書處理相關釋例（函釋、院長電子信箱，更新至 115.2.23）
- 全國法規資料庫《行政程序法》：https://law.moj.gov.tw/LawClass/LawAll.aspx?media=print&pcode=A0030055
- 全國法規資料庫《訴願法》：https://law.moj.gov.tw/LawClass/LawAll.aspx?media=print&pcode=A0030020
- 國家發展委員會《行政院及所屬各機關處理人民陳情案件要點》：https://theme.ndc.gov.tw/lawout/LawContent.aspx?id=GL000017

## 支持這個專案

如果這個工具對你有幫助：

- 按個 [Star](https://github.com/Imbad0202/tw-formal-writing) 讓更多人看到
- 分享給同事、同學、或任何需要寫公文的人
- [Buy Me a Coffee](https://buymeacoffee.com/crucify020v) 支持開發者持續更新
- 發現問題或有建議？歡迎開 [Issue](https://github.com/Imbad0202/tw-formal-writing/issues)

## 作者

**Cheng-I Wu** — [GitHub](https://github.com/Imbad0202) | [Buy Me a Coffee](https://buymeacoffee.com/crucify020v)

## 授權

[MIT License](LICENSE) — 自由使用、修改、分享。
