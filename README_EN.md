English | **[中文](README.md)**

# Taiwan Official Document Writing AI Skill

[![Version](https://img.shields.io/badge/version-v1.1.0-blue)](https://github.com/Imbad0202/tw-formal-writing/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Sponsor](https://img.shields.io/badge/sponsor-Buy%20Me%20a%20Coffee-orange?logo=buy-me-a-coffee)](https://buymeacoffee.com/crucify020v)

## Why does formal document writing matter?

In Taiwan, official documents follow strict rules governed by the *Official Document Format Act* and the *Document Processing Handbook*. Getting them wrong has real consequences.

**For government employees:**
- New civil servants receive minimal training — they learn by getting documents rejected and rewritten
- Using the wrong honorific (鈞 vs 貴), citation verb (奉 vs 據), or closing phrase can be seen as disrespectful to superiors
- Choosing the wrong processing method (先簽後稿 vs 簽稿併陳) means the entire workflow restarts
- Abolished phrases still slip in, and supervisors send them back

**For regular citizens and foreigners:**
- You want to petition the government, apply for a permit, or file an appeal — but have no idea how to format it
- You need to send a certified letter (存證信函) to your landlord but aren't sure about the legal phrasing
- An administrative appeal (訴願書) has a strict 30-day legal deadline — if the format is rejected, you may miss it

**What this Skill solves:**
- Import it into your AI tool (ChatGPT, Claude, Gemini), describe your situation in plain language, and get a properly formatted document that follows all regulations
- Correct terminology, format, and processing method are selected automatically
- Built-in quality checks catch common mistakes before you submit
- Already written a document? Paste it in and the AI will review and correct it

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
| `STANDALONE.md` | ~26K characters | File upload (full version with quality checks) |
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
# Method A: Global install (available in all projects)
mkdir -p ~/.claude/skills
git clone https://github.com/Imbad0202/tw-formal-writing.git ~/.claude/skills/tw-formal-writing

# Method B: Project-level install
mkdir -p .claude/skills
git clone https://github.com/Imbad0202/tw-formal-writing.git .claude/skills/tw-formal-writing
```

### Gemini Gems

1. Go to [Gemini](https://gemini.google.com) → Gems → Create a new Gem
2. Paste the entire contents of `STANDALONE.md` into the instructions field (~26K characters, approaching Gems' ~30K limit)

## Important Notice

> **Per the [Executive Yuan Guidelines on Generative AI Use by Government Agencies](https://www.ey.gov.tw/Page/448DE008087A1971/40c1a925-121d-4b6b-8f40-7e9e1a5401f2), classified documents must be written by the responsible officer and may not be produced using generative AI. Do not input classified information, non-public restricted information, or unnecessary personal data into this tool. For citizen-to-government documents, provide only the minimum identifying and contact details required for that procedure; avoid national ID numbers, ID-card scans, or similar high-sensitivity data unless a law, agency form, or workflow explicitly requires them.**

## Example Prompts

After importing, just tell the AI what you need:

- "I need to write a petition to the Taipei City Government about a noise complaint in my neighborhood"
- "Help me draft an application letter to the local district office to apply for a residence certificate"
- "I want to send a certified letter (存證信函) to my landlord demanding the return of my deposit"
- "How do I write a formal appeal (訴願書) against a traffic fine?"
- "I need to write a formal application (申請書) for a street vendor permit"

You can describe your situation in English — the AI will ask clarifying questions and generate the formal document in proper Chinese, following Taiwanese formatting rules, plus a separate explanation/translation for your reference. Submit the Chinese formal document after checking whether the receiving agency requires a standard form or extra attachments.

## For Foreigners in Taiwan

If you're a foreigner living or working in Taiwan and need to write formal documents to government agencies, this skill can help. Common scenarios:

- **Petitioning a government office** about a local issue (noise, construction, public safety)
- **Applying for permits or certificates** at district offices
- **Sending a certified letter** (存證信函) to a landlord, employer, or business
- **Filing an administrative appeal** (訴願) against a government decision
- **Writing a formal application** (申請書) for various government services

The AI communicates with you in English but generates the formal document in Traditional Chinese, as required by Taiwanese regulations. It can also provide a separate paragraph-by-paragraph English explanation so you understand what you're submitting, but that explanation should stay separate from the filing version.

## Regulatory Basis

- Executive Yuan "Document Processing Handbook" (文書處理手冊, revised June 8, 2023)
- "Official Document Format Act" (公文程式條例)
- National Academy of Civil Service "Official Document Writing Guide" (公文撰作解析, December 2025 edition)
- Official interpretations and rulings (文書處理相關釋例, updated to February 23, 2026)
- Administrative Procedure Act (official text): https://law.moj.gov.tw/LawClass/LawAll.aspx?media=print&pcode=A0030055
- Administrative Appeal Act (official text): https://law.moj.gov.tw/LawClass/LawAll.aspx?media=print&pcode=A0030020
- Directions for Handling Public Petitions by Executive Yuan Agencies: https://theme.ndc.gov.tw/lawout/LawContent.aspx?id=GL000017

## Support This Project

If this tool helped you:

- Hit [Star](https://github.com/Imbad0202/tw-formal-writing) so more people can find it
- Share with colleagues, classmates, or anyone who needs to write formal documents in Taiwan
- [Buy Me a Coffee](https://buymeacoffee.com/crucify020v) to support ongoing development
- Found a bug or have a suggestion? Open an [Issue](https://github.com/Imbad0202/tw-formal-writing/issues)

## Author

**Cheng-I Wu** — [GitHub](https://github.com/Imbad0202) | [Buy Me a Coffee](https://buymeacoffee.com/crucify020v)

## License

[MIT License](LICENSE) — free to use, modify, and share.
