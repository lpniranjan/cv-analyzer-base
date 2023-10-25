import streamlit as st
from dotenv import load_dotenv
import ResumeHandler as ResumeAnalasis
from HTMLTemplate import css, CV_template, ANA_template

#def HandleUserQuestion(userQuestion):
#     questionResponse = st.session_state.conversation({'question':userQuestion})
#     st.write(questionResponse)

load_dotenv()
st.set_page_config(page_title="CV Screening", page_icon=":document:")
st.write(css, unsafe_allow_html=True)

if "userQuestion" not in st.session_state:
     st.session_state['userQuestion'] = ''

with st.sidebar:
     st.subheader("Job Profile")
     jobTitle = st.text_input("Job title:")
     st.text_input("Experience level:")
     st.text_input("Communication level:")
     st.text_input("Company culture:")
     st.subheader("Candidate Profile")
     pdf_doc = st.file_uploader("Upload your candidate resume here and click 'Forecast'",accept_multiple_files=False)
     
st.header("Analysis of candidate resume")
if st.sidebar.button("Forecast"):
     if jobTitle and pdf_doc:
          st.session_state['userQuestion'] = "Please analyze this resume for  "+jobTitle+" post"
          st.text_input("Forecast this candidate based on:",st.session_state['userQuestion'])   
          with st.spinner("Analyzing"):
               resumeAnalysisData = ResumeAnalasis.GetSingleResumeResult(pdf_doc,st.session_state['userQuestion'],jobTitle)
               for x,y in resumeAnalysisData.items():
                    jobDescription = st.text_area("Job description:",(y[0]["jobDescription"]).strip(),height=100)                    
                    st.write(CV_template.replace("{{MSG}}", "Resume forecast:"),unsafe_allow_html=True)
                    st.write(ANA_template.replace("{{MSG}}", (y[0]["analysis"]).strip()),unsafe_allow_html=True)
                    st.sidebar.text_input("LinkedIn profile:",(y[0]["linkedinURL"]).strip())
                    st.sidebar.text_input("FaceBook profile:",(y[0]["facebookURL"]).strip())
                    st.sidebar.text_input("Github account:",(y[0]["githubURL"]).strip())
                    st.sidebar.text_input("Hackerank:")
                    st.sidebar.text_input("SO:")
     else:
          st.error('Please check whether "job title" inserted and "Resume" uploaded', icon="⚠️")                    
              
 

