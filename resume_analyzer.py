import streamlit as st
import pdfplumber
from docx import Document
from google import genai

# Page Config (Sirf ek baar, sabse upar)
st.set_page_config(page_title="AI Resume Analyzer", page_icon="🤖", layout="wide")

# API Key Secrets se uthana (Yahi best tareeqa hai)
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

st.title("🤖 Resume Checker")
st.markdown("Upload your resume and get an instant professional analysis!")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    job_description = st.text_area("Target Job Description (Optional)", placeholder="Paste target job description here...")

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

# Analyze Button
if st.button("🚀 Analyze Resume", type="primary"):
    if not GEMINI_API_KEY:
        st.error("API Key missing! Check your Streamlit Secrets.")
    elif uploaded_file is None:
        st.warning("Please upload a resume file first.")
    else:
        with st.spinner("Analyzing..."):
            # Text extraction
            if uploaded_file.name.endswith(".pdf"):
                resume_text = extract_text_from_pdf(uploaded_file)
            else:
                resume_text = extract_text_from_docx(uploaded_file)

            if not resume_text.strip():
                st.error("Could not read text from the resume.")
            else:
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt = f"""
                    You are an expert ATS and Career Coach. Analyze the given resume and provide a detailed report strictly in English:
                    
                    Resume Text: {resume_text}
                    Job Description: {job_description if job_description else "N/A"}
                    
                    Please structure your response with:
                    1. ATS Score (0-100)
                    2. Strengths
                    3. Weaknesses/Areas for Improvement
                    4. Missing Keywords
                    5. Career Recommendations
                    """
                    
                    response = client.models.generate_content(
                        model='gemini-2.0-flash', # Note: gemini-3.6-flash abhi available nahi hai, 2.0-flash use karein
                        contents=prompt
                    )
                    
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")