<div align="center">

<img src="assets/demo.gif" alt="AI Resume Analyzer Demo" width="800"/>

# 📄 AI Resume Analyzer

### Intelligent Resume-to-JD Matching Powered by Google Gemini AI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Gemini AI](https://img.shields.io/badge/Google-Gemini_AI-4285F4?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-brightgreen)](https://github.com/akash-dev-ai-brat/ai-resume-analyzer)

**AI Resume Analyzer** uses Google Gemini AI to analyze your resume against a job description, delivering an ATS compatibility score, gap analysis, tailored improvement suggestions, and keyword matching — in seconds.

[Live Demo](#) · [Report Bug](https://github.com/akash-dev-ai-brat/ai-resume-analyzer/issues) · [Request Feature](https://github.com/akash-dev-ai-brat/ai-resume-analyzer/issues)

</div>

---

## 📌 Table of Contents
- [About the Project](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## 🎯 About the Project <a name="about"></a>

Over 75% of resumes are rejected by ATS systems before a human ever reads them. AI Resume Analyzer solves this by using Google Gemini's multimodal intelligence to parse your resume PDF, compare it semantically against any job description, and generate actionable, specific feedback — not generic tips.

Whether you're a student applying for your first internship or a professional switching domains, this tool gives you a data-driven edge in the job market.

---

## ✨ Features <a name="features"></a>

- 📎 **PDF resume upload** — direct PDF parsing, no manual copy-pasting
- 🎯 **ATS compatibility score** — percentage match between your resume and the JD
- 🔍 **Keyword gap analysis** — missing keywords from the JD highlighted clearly
- 💡 **AI improvement suggestions** — specific, actionable rewrite advice per section
- 📝 **JD summary** — Gemini extracts the top required skills from any job posting
- ⚡ **Instant results** — full analysis in under 10 seconds

---

## 🛠️ Tech Stack <a name="tech-stack"></a>

| Layer | Technology |
|-------|-----------|
| AI / LLM | Google Gemini 1.5 Flash |
| PDF Parsing | PyMuPDF (fitz) / pdf2image |
| Frontend | Streamlit |
| Language | Python 3.10+ |
| API | Google Generative AI SDK |

---

## 📁 Project Structure <a name="project-structure"></a>

```
ai-resume-analyzer/
├── app.py                  # Streamlit app — main entry point
├── src/
│   ├── gemini_client.py    # Gemini API wrapper & prompt engineering
│   ├── pdf_parser.py       # PDF text + image extraction
│   └── analyzer.py         # Resume-JD comparison logic
├── prompts/
│   └── analysis_prompt.txt # System prompt for Gemini
├── assets/
│   └── demo.gif
├── .env.example            # Environment variable template
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start <a name="quick-start"></a>

**1. Clone the repository**
```bash
git clone https://github.com/akash-dev-ai-brat/ai-resume-analyzer.git
cd ai-resume-analyzer
```

**2. Set up your Gemini API key**
```bash
cp .env.example .env
# Add your key: GOOGLE_API_KEY=your_key_here
```
Get your free API key at [aistudio.google.com](https://aistudio.google.com)

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
streamlit run app.py
```

---

## ⚙️ How It Works <a name="how-it-works"></a>

```
User uploads Resume PDF + pastes Job Description
              │
              ▼
    PDF → Text + Images extracted
              │
              ▼
  Gemini 1.5 Flash receives both as input
              │
              ▼
  Structured JSON response:
    • ATS Score (0–100)
    • Missing Keywords list
    • Section-by-section feedback
    • Strength highlights
              │
              ▼
    Streamlit renders results dashboard
```

---

## 📋 Example Output <a name="example-output"></a>

```
✅ ATS Score: 73/100

🔑 Missing Keywords:
  - "RAG", "LangChain", "vector database", "MLOps"

📝 Suggestions:
  Projects section: Add quantified impact (e.g., "reduced latency by 40%")
  Skills section: Group by category (ML, Web Dev, Tools) for ATS clarity
  Summary: Lead with your target role — currently too generic

💪 Strengths:
  - Strong project diversity covering CV, NLP, and full-stack
  - Clear tech stack per project
```

---

## 📸 Screenshots <a name="screenshots"></a>


(assets/Screenshot 2026-05-23 000956.png)
(assets/Screenshot 2026-05-23 001104.png)
(assets/Screenshot 2026-05-23 001220.png)
(assets/Screenshot 2026-05-23 001246.png)
(assets/Screenshot 2026-05-23 001327.png)
(assets/Screenshot 2026-05-23 142329.png)
(assets/Screenshot 2026-05-23 142415.png)

---

## 🔮 Future Improvements <a name="future-improvements"></a>

- [ ] Auto-generate a rewritten resume section based on the JD
- [ ] Support for multiple JD comparison (batch mode)
- [ ] LinkedIn profile URL input (not just PDF)
- [ ] Export analysis report as PDF

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/akash-dev-ai-brat">Akash Nath</a> · 
  <a href="https://www.linkedin.com/in/akash-nath-5aa816293/">LinkedIn</a>
</div>
