# 台灣正式文件撰寫 AI Skill

# Taiwan Official Document Writing AI Skill

讓 AI 幫你寫出符合規範的台灣公文與正式文件。匯入你慣用的 AI 工具，描述情境就能產出格式正確、用語合規的公文。

Import this skill into your preferred AI tool to generate properly formatted Taiwanese government documents and formal correspondence. Just describe what you need — the AI handles formatting, terminology, and compliance automatically.

## 涵蓋範圍 / Coverage

| 類別 Category | 文件類型 Document Types |
|-----|--------|
| 政府公文 Government Official Documents | 簽 (Internal Memo)、函 (Official Letter)、書函 (Simple Letter)、令 (Decree)、呈 (Report to President)、咨 (Presidential Correspondence)、公告 (Public Announcement)、箋函 (Courtesy Letter)、便簽 (Internal Note) |
| 政府其他文件 Other Government Documents | 會議紀錄 (Meeting Minutes)、開會通知單 (Meeting Notice)、新聞稿 (Press Release)、施政報告 (Policy Report)、聘函 (Appointment Letter)、獎狀 (Certificate of Award) |
| 法律文件 Legal Documents | 存證信函 (Certified Letter)、合約書 (Contract)、律師函 (Lawyer's Letter)、備忘錄 MOU、聲明書 (Declaration)、切結書 (Affidavit)、委託書 (Power of Attorney) |
| 人民對政府 Citizen-to-Government | 陳情書 (Petition)、申請書 (Application)、訴願書 (Administrative Appeal)、異議書 (Objection) |

## 三個版本 / Three Versions

| 檔案 File | 大小 Size | 適用場景 Use Case |
|-----|-----|--------|
| `LITE.md` | ~2K 中文字 | ChatGPT GPTs Instructions（有字數限制 / size-limited fields） |
| `STANDALONE.md` | ~20K 中文字 | 檔案上傳（完整版，含品質檢核）/ File upload (full version with quality checks) |
| `SKILL.md` + `references/` | 多檔案 Multi-file | Claude Code 等支援多檔案的工具 / Tools that support multi-file skills |

## 匯入方式 / Setup Instructions

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
# 方法 A：複製到 commands 目錄
cp -r tw-formal-writing/ ~/.claude/commands/tw-formal-writing/

# 方法 B：在專案中使用
# 將 SKILL.md 和 references/ 放在專案根目錄的 .claude/ 下
```

### Gemini Gems

1. 前往 [Gemini](https://gemini.google.com) → Gems → 新建 Gem
2. 將 `STANDALONE.md` 的全部內容貼入指示欄位（~20K 字，Gems 上限 ~30K 字，放得下）

## 使用範例 / Example Prompts

貼入或上傳完成後，直接跟 AI 說：
After importing, just tell the AI what you need:

**中文 Chinese:**
- 「我是衛生局的承辦人，需要發函通知各醫療院所下個月要交傳染病統計表」
- 「幫我寫一份簽呈給局長，報告今年度預算執行情形」
- 「我要公告裁罰違規食品業者的結果」
- 「我想寄存證信函催房東退還押金」
- 「幫我寫陳情書向市政府反映噪音問題」

**English (for foreigners in Taiwan):**
- "I need to write a petition to the Taipei City Government about a noise complaint in my neighborhood"
- "Help me draft an application letter to the local district office to apply for a residence certificate"
- "I want to send a certified letter (存證信函) to my landlord demanding the return of my deposit"
- "How do I write a formal appeal (訴願書) against a traffic fine?"

AI 會自動判斷文件類別、確認必要資訊、產出合規文件、執行品質檢核。
The AI will identify the document type, confirm details, generate a compliant document in Chinese, and run quality checks. Even if you describe your situation in English, the output will be in proper formal Chinese as required by Taiwanese regulations.

## 依據 / Regulatory Basis

- 行政院《文書處理手冊》Executive Yuan "Document Processing Handbook" (revised June 8, 2023)
- 《公文程式條例》"Official Document Format Act"
- 國家文官學院《公文撰作解析》National Academy of Civil Service "Official Document Writing Guide" (December 2025 edition)
- 文書處理相關釋例 Official interpretations and rulings (updated to February 23, 2026)

## For Foreigners in Taiwan / 在台外國人指南

If you're a foreigner living or working in Taiwan and need to write formal documents to government agencies, this skill can help. Common scenarios:

- **Petitioning a government office** about a local issue (noise, construction, public safety)
- **Applying for permits or certificates** at district offices
- **Sending a certified letter** (存證信函) to a landlord, employer, or business
- **Filing an administrative appeal** (訴願) against a government decision
- **Writing a formal application** (申請書) for various government services

You can describe your situation in English — the AI will ask clarifying questions and generate the document in proper formal Chinese, following all Taiwanese government formatting rules. The output is ready to submit.
