import streamlit as st
import requests
import pandas as pd
import os

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://127.0.0.1:5000')

st.title("Score CV")
st.write("Upload multiple CVs and one Job Description to see a ranked list of candidates.")

# Helper to get mimetype
def get_mimetype(file_type: str) -> str:
    """Get mimetype from file type."""
    mimetype_map = {
        "application/pdf": "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    return mimetype_map.get(file_type, "text/plain")

# File Uploaders
st.subheader("Upload Documents")
# Allow multiple CVs to be uploaded
cv_files = st.file_uploader("Upload your CVs (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"], accept_multiple_files=True)
jd_file = st.file_uploader("Upload the Job Description (PDF, DOCX, TXT):", type=["pdf", "docx", "txt"])

if st.button("Analyze Documents"):
    # Check if files have been uploaded
    if cv_files and jd_file:
        results = []
        total_files = len(cv_files)
        progress_bar = st.progress(0)
        
        with st.spinner(f'Analyzing {total_files} CV(s)...'):
            # Prepare the single JD file outside the loop
            jd_file_data = (jd_file.name, jd_file.getvalue(), get_mimetype(jd_file.type))

            for i, cv_file in enumerate(cv_files):
                try:
                    # Prepare the current CV file
                    cv_file_data = (cv_file.name, cv_file.getvalue(), get_mimetype(cv_file.type))
                    
                    files = {
                        "cv_file": cv_file_data,
                        "jd_file": jd_file_data
                    }

                    # --- 1. Classify CV ---
                    # The classification endpoint expects only the CV file
                    classify_files = {"cv_file": cv_file_data}
                    classify_response = requests.post(
                        f"{BACKEND_URL}/classify_cv_file", 
                        files=classify_files,
                        timeout=30
                    )
                    
                    category = "N/A"
                    if classify_response.status_code == 200:
                        category = classify_response.json().get('category', 'N/A')
                    else:
                        st.warning(f"Could not classify {cv_file.name}.")

                    # --- 2. Match CV with JD ---
                    match_response = requests.post(
                        f"{BACKEND_URL}/match_cv_jd_files", 
                        files=files,
                        timeout=30
                    )
                    
                    score = 0.0
                    if match_response.status_code == 200:
                        score = match_response.json().get('match_score', 0.0)
                    else:
                        st.warning(f"Could not score {cv_file.name}.")

                    # Append results for this CV
                    results.append({
                        "CV Filename": cv_file.name,
                        "Predicted Category": category,
                        "Match Score": score
                    })

                except requests.exceptions.ConnectionError:
                    st.error(f"Connection Error while processing {cv_file.name}. Is the backend running?")
                    break # Stop processing if backend is down
                except Exception as e:
                    st.error(f"An error occurred with {cv_file.name}: {e}")
                
                # Update progress bar
                progress_bar.progress((i + 1) / total_files)

        if results:
            st.subheader("Ranked Results")
            # Convert results to a DataFrame
            df = pd.DataFrame(results)
            # Sort by score descending
            df = df.sort_values(by="Match Score", ascending=False).reset_index(drop=True)
            # Format score as percentage (backend returns 0-100, so divide by 100 for percentage format)
            df["Match Score"] = df["Match Score"].apply(lambda x: f"{float(x)/100:.2%}")
            
            st.dataframe(df)
        else:
            st.info("Analysis complete, but no results to display.")

    else:
        st.warning("Please upload at least one CV and a Job Description.")