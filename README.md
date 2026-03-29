# 台灣正式文件撰寫 AI Skill

讓 AI 幫你寫出符合規範的台灣公文與正式文件。

匯入你慣用的 AI 工具，描述情境就能產出格式正確、用語合規的公文。

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
| `LITE.md` | ~2K 中文字 | 有字數限制的 Instructions 欄位 |
| `STANDALONE.md` | ~20K 中文字 | 檔案上傳（完整版，含品質檢核） |
| `SKILL.md` + `references/` | 多檔案 | 支援多檔案的 AI 工具 |

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
# 方法 A：複製到 commands 目錄
cp -r tw-formal-writing/ ~/.claude/commands/tw-formal-writing/

# 方法 B：在專案中使用
# 將 SKILL.md 和 references/ 放在專案根目錄的 .claude/ 下
```

### Gemini Gems

1. 前往 [Gemini](https://gemini.google.com) → Gems → 新建 Gem
2. 將 `STANDALONE.md` 的全部內容貼入指示欄位（~20K 字，Gems 上限 ~30K 字，放得下）

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
