import streamlit as st
from google import genai
from google.genai import types
import fitz
import os
import json
import re
from dotenv import load_dotenv

# ─── Load API Key ──────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Resume Analyzer | Akash Nath",
    page_icon="🤖",
    layout="wide"
)

# ─── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.hero {
    background: linear-gradient(135deg, #0a1a0a, #0f2a0f, #1a3a0a);
    border-radius: 20px; padding: 40px; text-align: center;
    margin-bottom: 28px; border: 1px solid #4ade8030;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.hero-title {
    font-size: 2.8em; font-weight: 700;
    background: linear-gradient(90deg, #4ade80, #facc15, #86efac);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-sub { color: #86efac99; font-size: 1.05em; margin-top: 8px; }
.badge {
    display: inline-block;
    background: linear-gradient(90deg, #16a34a, #ca8a04);
    color: white; padding: 4px 16px; border-radius: 20px;
    font-size: 0.82em; font-weight: 700; margin-top: 12px;
}
.card {
    background: #0f1f0f; border-radius: 16px; padding: 24px;
    border: 1px solid #4ade8020; margin-bottom: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
.score-ring-container { text-align: center; padding: 20px; }
.score-number { font-size: 5em; font-weight: 800; line-height: 1; }
.score-label { font-size: 1em; color: #86efac99; margin-top: 6px; }
.section-title {
    font-size: 0.88em; font-weight: 600; letter-spacing: 1.5px;
    text-transform: uppercase; margin-bottom: 12px;
}
.tag {
    display: inline-block; padding: 5px 12px; border-radius: 20px;
    font-size: 0.82em; font-weight: 600; margin: 4px;
}
.tag-green  { background: #4ade8022; color: #4ade80; border: 1px solid #4ade8055; }
.tag-red    { background: #f8717122; color: #f87171; border: 1px solid #f8717155; }
.tag-yellow { background: #facc1522; color: #facc15; border: 1px solid #facc1555; }
.tag-blue   { background: #86efac22; color: #86efac; border: 1px solid #86efac55; }

.progress-bar-bg {
    background: #ffffff10; border-radius: 10px;
    height: 12px; margin: 8px 0; overflow: hidden;
}
.progress-bar-fill {
    height: 100%; border-radius: 10px;
    background: linear-gradient(90deg, #16a34a, #facc15);
}
.tip-item {
    background: #0a1a0a; border-radius: 10px;
    padding: 12px 16px; margin: 8px 0;
    border-left: 4px solid #facc15;
    color: #cceecc; font-size: 0.9em;
}
.strength-item {
    background: #0a1a0a; border-radius: 10px;
    padding: 12px 16px; margin: 8px 0;
    border-left: 4px solid #4ade80;
    color: #cceecc; font-size: 0.9em;
}
.stButton > button {
    background: linear-gradient(90deg, #16a34a, #ca8a04) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important; padding: 12px 28px !important;
    font-weight: 700 !important; font-size: 1.05em !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.85 !important; }
div[data-testid="stFileUploader"] {
    background: #0f1f0f !important;
    border: 2px dashed #4ade80 !important;
    border-radius: 16px !important; padding: 16px !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0f1f0f;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] { color: #86efac; }
.stTabs [aria-selected="true"] {
    color: #4ade80 !important;
    border-bottom-color: #4ade80 !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Helpers ───────────────────────────────────────────────────
def extract_pdf_text(uploaded_file):
    pdf_bytes = uploaded_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def parse_response(text):
    try:
        clean = re.sub(r"```json|```", "", text).strip()
        return json.loads(clean)
    except:
        return None

def score_color(score):
    if score >= 80: return "#4ade80"
    if score >= 60: return "#facc15"
    if score >= 40: return "#f97316"
    return "#f87171"

def score_label(score):
    if score >= 80: return ("🏆", "Excellent Match!")
    if score >= 60: return ("⭐", "Good Match")
    if score >= 40: return ("📈", "Moderate Match")
    return ("⚠️", "Needs Improvement")

# ─── HERO ──────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <div class='hero-title'>🤖 AI Resume Analyzer</div>
    <div class='hero-sub'>Upload your resume and a job description — AI scores your match instantly</div>
    <div class='badge'>Built by Akash Nath · AI & Data Science</div>
</div>
""", unsafe_allow_html=True)

# ─── INPUTS ────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title' style='color:#4ade80'>📄 Upload Your Resume</div>",
                unsafe_allow_html=True)
    uploaded_resume = st.file_uploader("", type=["pdf"], label_visibility="collapsed")
    if uploaded_resume:
        st.success(f"✅ {uploaded_resume.name} uploaded!")
    st.markdown("""
    <div style='background:#0a1a0a; border-radius:10px; padding:12px 16px;
    border-left:4px solid #4ade80; color:#86efac99; font-size:0.87em; margin-top:10px'>
        💡 Upload your resume as a <b>PDF file</b> for best results
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title' style='color:#facc15'>💼 Paste Job Description</div>",
                unsafe_allow_html=True)
    job_desc = st.text_area(
        "",
        placeholder="Paste the full job description here...\n\nExample:\nWe are looking for a Data Science Intern with skills in Python, Machine Learning, Pandas, SQL...",
        height=180,
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ─── BUTTON ────────────────────────────────────────────────────
analyze_btn = st.button("🚀 Analyze My Resume!")

# ─── RESULTS ───────────────────────────────────────────────────
if analyze_btn:
    if not uploaded_resume:
        st.warning("⚠️ Please upload your resume PDF!")
    elif not job_desc.strip():
        st.warning("⚠️ Please paste a job description!")
    else:
        with st.spinner("🤖 AI is analyzing your resume... this takes 10-15 seconds"):
            resume_text = extract_pdf_text(uploaded_resume)
            prompt = f"""
You are an expert ATS (Applicant Tracking System) and career coach.
Analyze the resume against the job description and respond ONLY in valid JSON.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_desc[:2000]}

Respond with ONLY this JSON structure, no extra text:
{{
    "match_score": <integer 0-100>,
    "score_breakdown": {{
        "skills_match": <integer 0-100>,
        "experience_match": <integer 0-100>,
        "education_match": <integer 0-100>,
        "keywords_match": <integer 0-100>
    }},
    "matched_keywords": [<list of keywords found in both resume and JD, max 10>],
    "missing_keywords": [<list of important keywords from JD missing in resume, max 10>],
    "strengths": [<list of 3-4 resume strengths for this role>],
    "improvements": [<list of 3-4 specific actionable improvements>],
    "verdict": "<one sentence overall verdict>",
    "recommended_role_level": "<Entry Level / Junior / Mid Level>"
}}
"""
            try:
                response = client.models.generate_content(
                    model="models/gemini-2.5-flash",
                    contents=prompt
                )
                data = parse_response(response.text)

                if not data:
                    st.error("❌ Could not parse AI response. Try again!")
                else:
                    score     = data.get("match_score", 0)
                    color     = score_color(score)
                    emoji, lbl= score_label(score)
                    breakdown = data.get("score_breakdown", {})

                    st.divider()

                    # ── Score + Breakdown + Verdict ────────────
                    r1, r2, r3 = st.columns([1, 1, 1], gap="large")

                    with r1:
                        st.markdown(f"""
                        <div class='card score-ring-container'>
                            <div style='font-size:2.5em'>{emoji}</div>
                            <div class='score-number' style='color:{color}'>{score}</div>
                            <div style='color:{color}; font-weight:700; font-size:1.1em'>/100</div>
                            <div class='score-label'>{lbl}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with r2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#facc15'>📊 Score Breakdown</div>",
                                    unsafe_allow_html=True)
                        for key, val in breakdown.items():
                            label_text = key.replace("_", " ").title()
                            bar_color  = score_color(val)
                            st.markdown(f"""
                            <div style='display:flex; justify-content:space-between; margin-bottom:2px'>
                                <span style='color:#cceecc; font-size:0.88em'>{label_text}</span>
                                <span style='color:{bar_color}; font-size:0.88em; font-weight:700'>{val}%</span>
                            </div>
                            <div class='progress-bar-bg'>
                                <div class='progress-bar-fill'
                                style='width:{val}%; background:linear-gradient(90deg,{bar_color},{bar_color}88)'>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with r3:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#4ade80'>🎯 Verdict</div>",
                                    unsafe_allow_html=True)
                        st.markdown(f"""
                        <div style='color:#cceecc; font-size:0.95em; line-height:1.6; margin-bottom:16px'>
                            {data.get("verdict", "")}
                        </div>
                        <div style='color:#86efac99; font-size:0.85em'>Recommended Level:</div>
                        <div style='color:#facc15; font-weight:700; font-size:1.1em; margin-top:4px'>
                            {data.get("recommended_role_level", "")}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    # ── Keywords ───────────────────────────────
                    k1, k2 = st.columns(2, gap="large")

                    with k1:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#4ade80'>✅ Matched Keywords</div>",
                                    unsafe_allow_html=True)
                        tags = "".join([f"<span class='tag tag-green'>{k}</span>"
                                        for k in data.get("matched_keywords", [])])
                        st.markdown(tags or "<span style='color:#555'>None found</span>",
                                    unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with k2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#f87171'>❌ Missing Keywords</div>",
                                    unsafe_allow_html=True)
                        tags = "".join([f"<span class='tag tag-red'>{k}</span>"
                                        for k in data.get("missing_keywords", [])])
                        st.markdown(tags or "<span style='color:#555'>None missing — great!</span>",
                                    unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    # ── Strengths & Improvements ───────────────
                    s1, s2 = st.columns(2, gap="large")

                    with s1:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#4ade80'>💪 Your Strengths</div>",
                                    unsafe_allow_html=True)
                        for s in data.get("strengths", []):
                            st.markdown(f"<div class='strength-item'>✅ {s}</div>",
                                        unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    with s2:
                        st.markdown("<div class='card'>", unsafe_allow_html=True)
                        st.markdown("<div class='section-title' style='color:#facc15'>🎯 How to Improve</div>",
                                    unsafe_allow_html=True)
                        for tip in data.get("improvements", []):
                            st.markdown(f"<div class='tip-item'>💡 {tip}</div>",
                                        unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Check your API key in the .env file")

# ─── Footer ────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; color:#4ade8055; font-size:0.85em; padding:30px 0 10px'>
    🤖 AI Resume Analyzer · Built with Python, Gemini AI & Streamlit ·
    <b style='color:#4ade80'>Akash Nath</b> · AI & Data Science
</div>
""", unsafe_allow_html=True)