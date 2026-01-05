import streamlit as st
import requests
import base64

st.title("Score CV")

st.write("This application classifies a CV and matches it against a Job Description.")

# CV Input
cv_file = st.file_uploader("Upload your CV (PDF):", type=["pdf"])

# JD Input
jd_file = st.file_uploader("Upload the Job Description (PDF or Text File):", type=["pdf", "txt"])

if st.button("Analyze"):
    if cv_file and jd_file:
        try:
            # Prepare files for upload
            files = {
                "cv_file": (cv_file.name, cv_file.getvalue(), "application/pdf"),
                "jd_file": (jd_file.name, jd_file.getvalue(), "application/pdf" if jd_file.type == "application/pdf" else "text/plain")
            }

            # 1. Classify CV
            classify_response = requests.post(
                "http://127.0.0.1:5000/classify_cv_file",
                files={"cv_file": files["cv_file"]}
            )
            if classify_response.status_code == 200:
                classification_result = classify_response.json()
                st.subheader("CV Classification")
                st.success(f"Predicted Category: **{classification_result['category']}**")
            else:
                st.error(f"Failed to classify CV: {classify_response.json().get('error', 'Unknown error')}")

            # 2. Match CV with JD
            match_response = requests.post(
                "http://127.0.0.1:5000/match_cv_jd_files",
                files=files
            )
            if match_response.status_code == 200:
                match_result = match_response.json()
                st.subheader("CV-JD Match Score")
                st.success(f"Match Score: **{match_result['match_score']:.2f}**")
                st.progress(match_result['match_score'])
            else:
                st.error(f"Failed to match CV and JD: {match_response.json().get('error', 'Unknown error')}")
                
        except requests.exceptions.ConnectionError as e:
            st.error(f"Connection Error: Could not connect to the backend. Please ensure the backend is running.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please upload both a CV and a Job Description.")