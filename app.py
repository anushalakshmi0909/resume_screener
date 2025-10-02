from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
from pdf2image import convert_from_bytes
import google.generativeai as genai

# Path to Poppler bin folder
poppler_path = os.getenv("POPPLER_PATH", r"C:\Users\anushalakshmi.s\poppler\poppler-25.07.0\Library\bin")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-latest')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)
        # images = pdf2image.convert_from_bytes(uploaded_file.read())
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
    
# Streamlit App

st.set_page_config(page_title="ATS Resume Screener", layout="wide")
st.header("ATS Resume Screener using Gemini Pro Vision")
input_text = st.text_area("Job Description", key="input", height=150)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
if uploaded_file is not None:
    st.write("PDF uploaded successfully.")

submit1 = st.button("What is the summary of the resume?")
submit2 = st.button("What are the key skills in the resume?")
submit3 = st.button("How well does the resume match the job description?")
submit4 = st.button("How can I improvise my skills to match the job description?")
submit5 = st.button("Rate the resume on a scale of 1-10 and provide a brief explanation.")

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

input_prompt_hr_multi_role = (
    "You are an experienced HR professional with extensive experience in evaluating candidates for technical roles in Data Science, Full Stack Development, DevOps, SDE, Data Analyst, Big Data Enginering and Cloud Computing. "
    "Given the candidate's resume and multiple job descriptions, analyze the candidate's strengths, weaknesses, and overall fit for each role from an HR perspective. "
    "For each role, provide:\n"
    "1. Key strengths relevant to the role\n"
    "2. Weaknesses or gaps that may affect performance\n"
    "3. HR insights on cultural fit, potential for growth, and readiness for the role\n"
    "4. A final recommendation (shortlist, interview, or training needed)\n\n"
    "Present the analysis role-wise in a clear and professional format suitable for HR decision-making."
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

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_hr_summary)
        st.text_area("Response", value=response, height=200)
    else:
        st.write("Please upload a resume PDF file.")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_strength_weakness)
        st.text_area("Response", value=response, height=200)
    else:
        st.write("Please upload a resume PDF file.")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_fit)
        st.text_area("Response", value=response, height=200)
    else:
        st.write("Please upload a resume PDF file.")
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_skills_gap)
        st.text_area("Response", value=response, height=200)
    else:
        st.write("Please upload a resume PDF file.")
elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt_ats_scanner)
        st.text_area("Response", value=response, height=200)
    else:
        st.write("Please upload a resume PDF file.")

prompt = st.text_area("Enter your prompt", height=100, value="Based on the job description, rate the resume on a scale of 1-10 and provide a brief explanation.")