import streamlit as st
import pdfplumber
from docx import Document
from google import genai

# Page Config
st.set_page_config(
    page_title="AI Resume Pro - ATS Optimizer", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Neon & Gradient Custom CSS for Ultra-Modern Look
st.markdown("""
<style>
    /* Main Background Accent */
    .stApp {
        background: radial-gradient(circle at top left, #0f172a, #1e1b4b, #090d16);
        color: #f8fafc;
    }
    
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.4);
        margin-bottom: 2rem;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
    }

    /* Custom Glowing Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #db2777 0%, #7c3aed 100%);
        box-shadow: 0 6px 20px rgba(236, 72, 153, 0.6);
        transform: translateY(-2px);
        color: white;
    }

    /* Card Box Styling */
    .custom-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
    }
    
    /* Sidebar custom look */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with Rich Graphics & Badges
with st.sidebar:
    st.markdown("### 🔥 AI Career Suite")
    st.markdown("---")
    st.markdown("✨ **Features:**")
    st.markdown("🎯 **Instant ATS Score**")
    st.markdown("💡 **Smart Keyword Match**")
    st.markdown("🚀 **Deep Weakness Analysis**")
    st.markdown("---")
    st.info("💡 **Pro Tip:** Paste the target job description to match your skills with 99% accuracy!")

# Hero Banner Header
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⚡ AI Resume Analyzer Pro</div>
    <div class="hero-subtitle">Transform your resume into an interview magnet using Next-Gen AI intelligence! 🚀</div>
</div>
""", unsafe_allow_html=True)

# API Key check from Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Input Layout using containers
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 📂 Step 1: Upload File")
    with st.container():
        uploaded_file = st.file_uploader("Upload PDF or Word Document", type=["pdf", "docx"])
        if uploaded_file:
            st.success(f"✅ Loaded: **{uploaded_file.name}**")

with col2:
    st.markdown("### 🎯 Step 2: Job Match (Optional)")
    with st.container():
        job_description = st.text_area(
            "Paste Job Description", 
            placeholder="Paste target job requirements here to find missing keywords...",
            height=125
        )

st.markdown("<br>", unsafe_allow_html=True)

# Helper Functions
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

# Centered Glowing Action Button
b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
with b_col2:
    analyze_btn = st.button("✨ Run Deep AI Analysis ✨", type="primary")

# Execution logic on Button Click
if analyze_btn:
    if not GEMINI_API_KEY:
        st.error("API Key missing! Please configure your Streamlit Secrets.")
    elif uploaded_file is None:
        st.warning("⚠️ Please upload a resume file first before analyzing!")
    else:
        with st.spinner("🔮 AI is scanning your resume, calculating ATS score & detecting gaps..."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)

            if not resume_text.strip():
                st.error("Could not read text from the uploaded file. Please try another file.")
            else:
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt = f"""
                    You are an elite ATS and Senior Career Coach. Analyze the given resume and provide a detailed report strictly in English:
                    
                    Resume Text: {resume_text}
                    Job Description: {job_description if job_description else "N/A"}
                    
                    Please structure your response with striking formatting:
                    1. ATS Score (0-100 with clear indicator)
                    2. Core Strengths (Bullet points with emojis)
                    3. Weaknesses/Areas for Improvement
                    4. Missing Keywords
                    5. Actionable Career Recommendations
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=prompt
                    )
                    
                    st.markdown("---")
                    st.markdown("### 📊 Comprehensive Analysis Report")
                    
                    # Display report inside a high-end styled glowing container
                    with st.container():
                        st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
