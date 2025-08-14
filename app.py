from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64
import fitz

genai.configure(api_key=os.getenv("Google_API_key"))

def get_gemini_response(job_desc, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([
        {"text": prompt},            # The main instruction
        {"text": "Job Description:\n" + job_desc},  # Job description text
        pdf_content[0]               # The resume first page image
    ])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Open PDF from uploaded file
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        first_page = pdf_document[0]  # Get first page
        pix = first_page.get_pixmap()
        img_byte_arr = io.BytesIO(pix.tobytes("jpeg"))

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr.getvalue()).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("no file uploaded")
    
##streamlit app
st.set_page_config(page_title="ATS Tracker")
st.header("ATS Tracking System")
input_text=st.text_area("Job Description : ",key="input")
uploaded_file=st.file_uploader("Upload your resume(PDF).....",type=['pdf'])

if uploaded_file is not None:
    st.write("Pdf uploaded Successfully")

submit1=st.button("Tell me about the resume")
submit2=st.button("How Can I Imporve my skills")
submit3=st.button("What are the keywords that are missing")
submit4=st.button("Percentage match")

input_prompt1 = """
You are an expert HR recruiter and career advisor.
Analyze the provided resume content and summarize:
1. The candidate's main skills
2. Work experience highlights
3. Education details
4. Overall career profile in 4-6 sentences
Focus on giving a professional summary that could be used in an interview introduction.
"""

input_prompt2 = """
You are a career mentor.
Review the resume and the job description.
Identify skill gaps between the candidate’s resume and the job requirements.
Give clear and practical suggestions to improve those skills, including:
- Technical skills to learn
- Certifications to pursue
- Projects or experience to gain
Format the answer in bullet points for easy reading.
"""

input_prompt3 = """
You are an ATS (Applicant Tracking System) optimization expert.
Compare the job description and the resume content.
List important keywords, skills, and industry terms from the job description that are missing in the resume.
These should be specific technical skills, tools, or role-related terms that would help the resume rank higher in ATS.
Return the answer as a simple bullet point list.
"""

input_prompt4 = """
You are an ATS scoring algorithm.
Compare the resume with the job description and calculate a match percentage based on:
- Skills overlap
- Relevant work experience
- Educational fit
- Industry-related keywords
Return:
1. The overall match percentage (0-100%)
2. A short explanation of why this score was given
"""
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("About the Resume")
        st.write(response)
    else:
        st.warning("Please upload the file")

if submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("Skill Improvement Suggestions")
        st.write(response)
    else:
        st.warning("Please upload the file")

if submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("Missing Keywords")
        st.write(response)
    else:
        st.warning("Please upload the file")

if submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("ATS Match Percentage")
        st.write(response)
    else:
        st.warning("Please upload the file")
