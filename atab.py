#main.py
import base64
import json
import pandas as pd
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai
from dotenv import load_dotenv
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import streamlit.components.v1 as components

# Load API key from environment variable
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
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
        except Exception as e:
            st.error(f"Error processing PDF: {e}")
        return None
    else:
        st.error("No file uploaded")
        return None

# ------------------ Streamlit UI Configuration ------------------ #

st.set_page_config(
    page_title="ATS SYSTEM",
    page_icon=":document:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ Sidebar ------------------ #

st.sidebar.header("ATS Resume Advisor")
st.sidebar.subheader("Supports resume creation based on ATS criteria")
st.sidebar.image(r"C:\Users\sudhirb\chatbot\bg\a.PNG")

# Options Menu
with st.sidebar:
    selected = option_menu('ATS', ["About", 'ATS', 'FAQs'],
                           icons=['play-btn', 'search', 'info-circle'], menu_icon='intersect', default_index=0)

# ------------------ Main App UI ------------------ #

tab1, tab2, tab3 = st.tabs(["About", "ATS", "FAQs"])

with tab1:
    st.header("Welcome to Gemini Resume Expert!")
    st.subheader("An AI-powered tool designed to help applicants better their resumes")
    st.markdown(
        "This Gemini based ATS scanner is a cutting-edge resume analysis and optimization tool designed to empower job seekers in the competitive Applicant Tracking System (ATS) landscape. Leveraging the power of LangChain advanced natural language processing and Google Gemini Pro capabilities, our system provides insightful analysis of your resume against job descriptions."
    )
    st.markdown(
        "Your one-stop shop for crafting ATS-optimized resumes and landing your dream job."
        "This leverages the power of cutting-edge artificial intelligence to analyze your resume against job descriptions and provide actionable insights to help you stand out in the applicant pool."
    )
    st.subheader("Here's how it works:")
    st.markdown("1. Upload your resume: Simply drag and drop your resume file or upload it from your computer.")
    st.markdown("2. Enter job description (optional): Provide the job description you're targeting for a more tailored analysis.")
    st.markdown("3. Get powerful analysis: Our system will analyze your resume and provide you with a comprehensive report.")

with tab2:
    st.title('ATS Insights')
    st.subheader('Upload the resume below and enter the job description to analyze the input resume and check HR and ATS perspective')

    # Two column layout for the main app content
    col1, col2 = st.columns([1, 1])

    with col1:
        job_roles = ["Software Engineer","GenAI", "Data Scientist", "Product Manager", "Designer", "Marketing Specialist"]
        selected_role = st.selectbox("Select Job Role", job_roles)
        input_text = st.text_area("Job Description", key="input")
        
    uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")

    if uploaded_file is not None:
        st.write("PDF Uploaded Successfully")

    analysis_choice = st.selectbox("Select Analysis Type",
                                   ["HR Manager Perspective", "ATS Scanner Perspective"])

    submit_button = st.button("Analyze")

input_prompt1 = """
You are an experienced Human Resource Manager, your task is to review the provided resume against the job description for a {role}.
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
As a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
evaluate the resume against the provided job description for a {role}. Give the percentage match if the resume matches
the job description. First the output should come as a percentage, then keywords missing and last final thoughts.
"""

def display_response(response):
    st.subheader("Analysis Result")
    st.write(response)

if submit_button:
    with st.spinner("Processing..."):
        pdf_content = input_pdf_setup(uploaded_file)
        if pdf_content:
            role = selected_role
            if analysis_choice == "HR Manager Perspective":
                prompt = input_prompt1.format(role=role)
            else:
                prompt = input_prompt2.format(role=role)
            response = get_gemini_response(input_text, pdf_content, prompt)
            display_response(response)

# Layout for displaying job description and resume side by side
if uploaded_file and input_text:
    st.markdown("## Comparison View")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Job Description")
        st.write(input_text)

    with col2:
        st.markdown("### Resume Preview")
        try:
            images = pdf2image.convert_from_bytes(uploaded_file.read())
            st.image(images[0], use_column_width=True)
        except Exception as e:
            st.error(e)

with tab3:
    st.title('Frequently Asked Questions(FAQs)')
    st.markdown(""" Q. What is Gemini resume expert?""")
    st.markdown("Ans. It is a resume analysis and optimization tool powered by artificial intelligence. It helps job seekers craft ATS-friendly resumes that stand out in the applicant pool.")
    st.markdown("Q. How does it work?")
    st.markdown("Ans. Simply upload your resume (and optionally a job description) and our system will analyze it to identify key areas for improvement. You'll receive a report with insights on skill gaps, keyword optimization, readability, and more.")
    st.markdown("Q. Is it free to use?")
    st.markdown("Ans. This may offer a free trial or basic functionalities. For more advanced features or in-depth analysis, there might be paid subscription options. Check the website for specific pricing details.")
    st.markdown("""---""")
    


    
