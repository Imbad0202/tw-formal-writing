English | **[中文](README.md)**

# Taiwan Official Document Writing AI Skill

Import this skill into your preferred AI tool to generate properly formatted Taiwanese government documents and formal correspondence. Just describe what you need — the AI handles formatting, terminology, and compliance automatically.

## Coverage

| Category | Document Types |
|----------|---------------|
| Government Official Documents | Internal Memo (簽), Official Letter (函), Simple Letter (書函), Decree (令), Report to President (呈), Presidential Correspondence (咨), Public Announcement (公告), Courtesy Letter (箋函), Internal Note (便簽) |
| Other Government Documents | Meeting Minutes (會議紀錄), Meeting Notice (開會通知單), Press Release (新聞稿), Policy Report (施政報告), Appointment Letter (聘函), Certificate of Award (獎狀) |
| Legal Documents | Certified Letter (存證信函), Contract (合約書), Lawyer's Letter (律師函), MOU (備忘錄), Declaration (聲明書), Affidavit (切結書), Power of Attorney (委託書) |
| Citizen-to-Government | Petition (陳情書), Application (申請書), Administrative Appeal (訴願書), Objection (異議書) |

## Three Versions

| File | Size | Use Case |
|------|------|----------|
| `LITE.md` | ~2K Chinese characters | ChatGPT GPTs Instructions (size-limited fields) |
| `STANDALONE.md` | ~20K Chinese characters | File upload (full version with quality checks) |
| `SKILL.md` + `references/` | Multi-file | Tools that support multi-file skills (Claude Code, etc.) |

## Setup Instructions

### ChatGPT GPTs

**Method A (Recommended): Upload the full version**
1. Go to [ChatGPT](https://chat.openai.com) → My GPTs → Create a GPT
2. In Configure → Knowledge, upload `STANDALONE.md`
3. Paste this into the Instructions field:
   ```
   You are a Taiwan formal document writing expert. Follow the rules in
   STANDALONE.md from Knowledge to help users write official documents and
   formal correspondence. First identify the document category, then write
   according to the corresponding rules. Run a quality check after generating.
   ```

**Method B: Paste the lite version directly**
1. Go to My GPTs → Create a GPT
2. Paste the entire contents of `LITE.md` into the Instructions field

### ChatGPT Projects

1. Go to ChatGPT → Projects → Create or select a Project
2. Upload `STANDALONE.md` as a Project File
3. Start chatting

### Claude (claude.ai)

1. Go to [Claude](https://claude.ai) → Projects → Create a new Project
2. Upload `STANDALONE.md` to Project Knowledge
3. Start chatting within that Project

### Claude Code

```bash
# Method A: Copy to commands directory
cp -r tw-formal-writing/ ~/.claude/commands/tw-formal-writing/

# Method B: Use in a project
# Place SKILL.md and references/ under .claude/ in your project root
```

### Gemini Gems

1. Go to [Gemini](https://gemini.google.com) → Gems → Create a new Gem
2. Paste the entire contents of `STANDALONE.md` into the instructions field (~20K characters, within Gems' ~30K limit)

## Example Prompts

After importing, just tell the AI what you need:

- "I need to write a petition to the Taipei City Government about a noise complaint in my neighborhood"
- "Help me draft an application letter to the local district office to apply for a residence certificate"
- "I want to send a certified letter (存證信函) to my landlord demanding the return of my deposit"
- "How do I write a formal appeal (訴願書) against a traffic fine?"
- "I need to write a formal application (申請書) for a street vendor permit"

You can describe your situation in English — the AI will ask clarifying questions and generate the document in proper formal Chinese, following all Taiwanese government formatting rules. The output is ready to submit.

## For Foreigners in Taiwan

If you're a foreigner living or working in Taiwan and need to write formal documents to government agencies, this skill can help. Common scenarios:

- **Petitioning a government office** about a local issue (noise, construction, public safety)
- **Applying for permits or certificates** at district offices
- **Sending a certified letter** (存證信函) to a landlord, employer, or business
- **Filing an administrative appeal** (訴願) against a government decision
- **Writing a formal application** (申請書) for various government services

The AI communicates with you in English but generates all documents in formal Traditional Chinese, as required by Taiwanese regulations. Each document includes a paragraph-by-paragraph English translation so you understand what you're submitting.

## Regulatory Basis

- Executive Yuan "Document Processing Handbook" (文書處理手冊, revised June 8, 2023)
- "Official Document Format Act" (公文程式條例)
- National Academy of Civil Service "Official Document Writing Guide" (公文撰作解析, December 2025 edition)
- Official interpretations and rulings (文書處理相關釋例, updated to February 23, 2026)
