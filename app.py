from dotenv import load_dotenv
import streamlit as st
import os
import io
import base64
from PIL import Image
from pdf2image import convert_from_bytes
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Path to Poppler bin folder
poppler_path = os.getenv("POPPLER_PATH", r"C:\Users\anushalakshmi.s\poppler\poppler-25.07.0\Library\bin")

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- Helper Functions ---
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-latest')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded.")

def display_response(title, response):
    st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div style="
            background-color:#f4f6f8; 
            padding:15px; 
            border-radius:10px; 
            border:1px solid #ccc; 
            font-size:15px; 
            line-height:1.6;
            color:#1c2833;
        ">
            {response.replace(chr(10), '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Streamlit App UI ---
st.set_page_config(page_title="ATS Resume Screener", layout="wide")

st.markdown("<h1 style='text-align: center; color: #2E86C1;'>📄 AI-Powered ATS Resume Screener</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area("📝 Job Description", key="input", height=250)

with col2:
    uploaded_file = st.file_uploader("📂 Upload Resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        st.success("✅ Resume uploaded successfully!")

st.divider()
st.markdown("### 🔍 Choose an Evaluation Type")

colA, colB, colC = st.columns(3)
with colA:
    submit1 = st.button("📌 Resume Summary")
    submit2 = st.button("🛠 Key Skills")
with colB:
    submit3 = st.button("⚖ Fit for Role")
    submit4 = st.button("📉 Skills Gap")
with colC:
    submit5 = st.button("⭐ ATS Scoring")

# --- Predefined Prompts ---
input_prompt_strength_weakness = (
    "You are an experienced HR professional with technical knowledge in Data Science, Full Stack Development, and Cloud Computing. "
    "Based on the resume and the job description provided, analyze the candidate's strengths and weaknesses specifically in relation to the requirements of this role. "
    "Provide a concise summary highlighting which skills, experiences, and qualifications make the candidate suitable, and which areas might need improvement."
)

input_prompt_fit = (
    "Act as a technical recruiter. Compare the candidate's resume with the given job description. "
    "Identify key strengths and weaknesses, and explain how well the candidate fits the role. "
    "Provide actionable recommendations on whether the candidate should be shortlisted, further trained, or considered for a different role."
)

input_prompt_alignment = (
    "You are an HR expert. Evaluate the candidate's resume against the provided job description. "
    "List the candidate’s strengths that directly match the role’s requirements, and weaknesses that could impact their performance. "
    "Provide a final assessment of the candidate's suitability for the position."
)

input_prompt_skills_gap = (
    "You are a professional recruiter with technical expertise. Analyze the resume and job description to identify the candidate’s strengths and technical skills, "
    "as well as any gaps or weaknesses in their experience or knowledge relevant to the job. "
    "Provide a clear summary that highlights both strong and weak areas."
)

input_prompt_hr_summary = (
    "You are an experienced HR manager with knowledge in Data Science, Full Stack, and Cloud Computing. "
    "Based on the resume and job description, provide a brief summary that clearly outlines the candidate’s main strengths, potential weaknesses, and overall suitability for the role."
)

input_prompt_ats_scanner = (
    "You are an automated Applicant Tracking System (ATS) that evaluates resumes for technical roles in Data Science, Full Stack Development, and Cloud Computing. "
    "Given a candidate's resume and a job description, perform the following analysis:\n"
    "1. Score the resume's match with the job description on a scale of 0 to 100.\n"
    "2. Highlight the keywords, skills, and qualifications present that match the job requirements.\n"
    "3. Identify missing or weak keywords and skills that reduce the match score.\n"
    "4. Provide a final recommendation: 'Highly Suitable', 'Moderately Suitable', or 'Not Suitable'.\n\n"
    "Present the output clearly and in a structured ATS-like format."
)

# --- Button Actions ---
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_hr_summary)
        display_response("📌 Resume Summary", response)
    else:
        st.warning("⚠ Please upload a resume PDF file.")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_strength_weakness)
        display_response("🛠 Key Skills", response)
    else:
        st.warning("⚠ Please upload a resume PDF file.")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_fit)
        display_response("⚖ Fit for Role", response)
    else:
        st.warning("⚠ Please upload a resume PDF file.")
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_skills_gap)
        display_response("📉 Skills Gap", response)
    else:
        st.warning("⚠ Please upload a resume PDF file.")
elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_ats_scanner)
        display_response("⭐ ATS Scoring", response)
    else:
        st.warning("⚠ Please upload a resume PDF file.")

# --- Custom Prompt Section ---
st.divider()
st.markdown("### ✨ Custom HR Prompt")

custom_prompt = st.text_area(
    "Enter your custom prompt for analysis:",
    height=120,
    placeholder="E.g., Suggest improvements for project section of the resume..."
)

if st.button("Run Custom Analysis"):
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, custom_prompt)
        display_response("✨ Custom Analysis Result", response)
    else:
        st.warning("⚠ Please upload a resume PDF file first.")
