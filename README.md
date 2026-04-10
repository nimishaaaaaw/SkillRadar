# 🎯 SkillRadar — AI-Powered Resume Screener

> *Paste your resume. Paste the JD. Know exactly where you stand.*

An NLP-powered resume screening tool that scores alignment between your resume and a job description, identifies skill gaps, and delivers AI-generated improvement suggestions — in seconds.

**🌐 Live App:** https://skillradar-591t.onrender.com

---

## 🚀 Deployment Status

[![Live on Render](https://img.shields.io/badge/Live-Render-46E3B7?logo=render&logoColor=white)](https://skillradar-591t.onrender.com)
[![AI - Groq LLaMA 3.1](https://img.shields.io/badge/AI-Groq%20LLaMA%203.1-FF85BB?logo=meta&logoColor=white)](https://groq.com)
[![NLP - Scikit-learn](https://img.shields.io/badge/NLP-Scikit--learn-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![GitHub Repo](https://img.shields.io/badge/GitHub-SkillRadar-181717?logo=github&logoColor=white)](https://github.com/nimishaaaaaw/SkillRadar)

---

## ✨ Features

- 🎯 **Match Score** — TF-IDF vectorisation + cosine similarity scores resume-JD alignment as a percentage, displayed with an animated score ring
- 🛠 **Tech Skills Analysis** — Cross-references both documents against a 200+ tech skills dictionary, returning matched and missing skills separately
- 🔍 **Keyword Analysis** — Extracts top keywords from both texts and shows matched, missing, and resume-only terms
- 📋 **Resume Quality Score** — Five independent checks (length, sections, action verbs, quantification, contact info) scored out of 100
- ✨ **AI Suggestions** — Calls Groq LLaMA 3.1 with gap context to generate 4 specific, actionable improvement suggestions per scan
- 📄 **PDF or Text Input** — Upload resume as a PDF or paste as plain text; JD always pasted as text
- ⏳ **Loading Overlay** — Smooth animated spinner while analysis runs
- 🎨 **Clean UI** — Space Grotesk + DM Sans fonts, navy and pink palette, gradient hero section

---

## 🛠 Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python_3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-154F5B?logo=python&logoColor=white)

### AI & NLP
![Groq](https://img.shields.io/badge/Groq_LLaMA_3.1-FF85BB?logo=meta&logoColor=white)
![TF-IDF](https://img.shields.io/badge/TF--IDF-Cosine_Similarity-021A54?logoColor=white)
![pdfplumber](https://img.shields.io/badge/pdfplumber-PDF_Parsing-red?logoColor=white)

### Frontend
![Bootstrap](https://img.shields.io/badge/Bootstrap_5-7952B3?logo=bootstrap&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)
![Google Fonts](https://img.shields.io/badge/Fonts-Space_Grotesk_+_DM_Sans-4285F4?logo=googlefonts&logoColor=white)

### Deployment
![Render](https://img.shields.io/badge/Render-46E3B7?logo=render&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?logo=gunicorn&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?logo=github&logoColor=white)

---

## 🧠 How It Works

```
User pastes resume + job description
              ↓
Text cleaned → stopwords removed → TF-IDF vectorised
              ↓
Cosine similarity → Match Score (0–100%)
              ↓
200+ skills dictionary → Matched vs Missing tech skills
              ↓
Top keyword extraction → Keyword gap analysis
              ↓
5-check rule engine → Resume Quality Score
              ↓
Missing context sent to Groq LLaMA 3.1 → 4 AI suggestions
              ↓
Results rendered with animated score ring
```

---

## 📸 Screenshots

### 🏠 Landing Page
![Landing](screenshots/Screenshot(2739).png)

### 📋 How It Works
![How It Works](screenshots/Screenshot(2740).png)

### 📝 Input Form
![Form](screenshots/Screenshot(2741).png)

### ⏳ Analysis Loading
![Loading](screenshots/Screenshot(2743).png)

### 📊 Results — Match Score & Tech Skills
![Results Score](screenshots/Screenshot(2744).png)

### 🔍 Results — Keyword Analysis & AI Suggestions
![Results Keywords](screenshots/Screenshot(2746).png)

### 📋 Results — Resume Quality Score
![Results Resume Score](screenshots/Screenshot(2747).png)

---

## 🗂 Project Structure

```
SkillRadar/
├── app/
│   ├── __init__.py          ← Flask app factory
│   ├── routes.py            ← URL routes and analysis orchestration
│   ├── nlp_engine.py        ← TF-IDF, cosine similarity, keyword extraction
│   ├── resume_scorer.py     ← 5-check resume quality scoring engine
│   ├── ai_service.py        ← Groq LLaMA 3.1 API integration
│   ├── pdf_utils.py         ← PDF text extraction with pdfplumber
│   ├── skills_list.py       ← 200+ tech skills dictionary
│   ├── static/
│   │   └── images/          ← Logo and assets
│   └── templates/
│       ├── base.html        ← Shared layout, navbar, fonts
│       ├── index.html       ← Landing page + input form
│       └── results.html     ← Full analysis results page
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── run.py
└── .env
```

---

## 🖥️ Run Locally

### Prerequisites
- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Git

### Clone & Setup
```bash
git clone https://github.com/nimishaaaaaw/SkillRadar.git
cd SkillRadar
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### Download NLTK Data
```bash
python -m nltk.downloader stopwords punkt punkt_tab
```

### Configure Environment
Create a `.env` file in the root:
```env
SECRET_KEY=your-secret-key
GROQ_API_KEY=your-groq-api-key
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run
```bash
python run.py
```
Visit `http://127.0.0.1:5000`

---

## 🐳 Docker

```bash
# Build and run
docker compose up --build

# Run in background
docker compose up -d

# Stop
docker compose down
```

Visit `http://127.0.0.1:5000`

---

## 📊 Resume Quality Checks

| Check | What It Evaluates | Max Score |
|---|---|---|
| Resume Length | Word count — ideal 300–700 words | 20 |
| Key Sections | Presence of experience, education, skills, projects | 20 |
| Action Verbs | Built, designed, deployed, optimised etc. | 20 |
| Quantification | Numbers, percentages, metrics like 300ms, 10+ users | 20 |
| Contact Info | Email, phone, LinkedIn, GitHub | 20 |

---

## 🤖 AI Suggestions

Missing skills and keywords are sent to **Groq LLaMA 3.1** along with the JD context. The model returns 4 specific, actionable suggestions — for example:

> *"Add PyTorch or TensorFlow to your skills section — the JD mentions deep learning frameworks 3 times."*

> *"Include your GCP or Azure exposure even if basic — cloud platform familiarity is explicitly required."*

Suggestions are parsed from a strict JSON response format and rendered as numbered cards on the results page.

---

## 📌 Future Improvements

- 📤 Export full analysis report as PDF
- 🕓 Scan history across sessions with local storage
- 🏷️ ATS keyword density scoring
- 🌍 Multi-language JD support
- 📱 Mobile-optimised layout improvements

---

## 👩‍💻 Author

**Nimisha Majgawali**

[![GitHub](https://img.shields.io/badge/GitHub-nimishaaaaaw-181717?logo=github)](https://github.com/nimishaaaaaw)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Nimisha_Majgawali-0A66C2?logo=linkedin)](https://www.linkedin.com/in/nimisha-majgawali-97420b315/)
