import streamlit as st
import pdfplumber
from docx import Document
from google import genai

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer Pro", 
    page_icon="🎯", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for gorgeous look & graphics
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #4F46E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        background: linear-gradient(90deg, #4F46E5 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 0.6rem 1rem;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #4338CA 0%, #2563EB 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for instructions / guide
with st.sidebar:
    st.image("https://img.icons8.com/color/96/resume.png", width=80)
    st.markdown("### 📌 Quick Guide:")
    st.markdown("1. **Upload Resume** (PDF or Word format).")
    st.markdown("2. *(Optional)* Paste target job description.")
    st.markdown("3. Click **Analyze Resume Now**.")
    st.markdown("---")
    st.markdown("💡 **Pro Tip:** Job description dalne se AI aur zyada accurate ATS score nikal kar deta hai!")

# Main Title Header
st.markdown('<p class="main-header">🎯 AI Resume Analyzer & ATS Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Supercharge your resume with advanced AI intelligence and get hired faster!</p>', unsafe_allow_html=True)

# API Key check from Streamlit Secrets
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# Main Interface with structured columns
with st.container():
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### 📄 Step 1: Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])
        if uploaded_file:
            st.success(f"File uploaded: **{uploaded_file.name}**")

    with col2:
        st.markdown("#### 💼 Step 2: Target Job Description")
        job_description = st.text_area(
            "Paste job description (Optional)", 
            placeholder="Paste target job requirements here to check compatibility...",
            height=130
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

# Centered Fancy Analyze Button
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_btn = st.button("🚀 Analyze Resume Now", type="primary")

# Execution logic on Button Click
if analyze_btn:
    if not GEMINI_API_KEY:
        st.error("API Key missing! Please configure your Streamlit Secrets.")
    elif uploaded_file is None:
        st.warning("⚠️ Please upload a resume file first before clicking analyze.")
    else:
        with st.spinner("🔄 Reading text and running deep AI analysis... Please wait."):
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)

            if not resume_text.strip():
                st.error("Could not read text from the uploaded resume. Please check the file.")
            else:
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt = f"""
                    You are an expert ATS and Senior Career Coach. Analyze the given resume and provide a detailed report strictly in English:
                    
                    Resume Text: {resume_text}
                    Job Description: {job_description if job_description else "N/A"}
                    
                    Please structure your response cleanly with markdown:
                    1. ATS Score (0-100)
                    2. Key Strengths
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
                    
                    # Display report inside a clean styled container
                    with st.container(border=True):
                        st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")
