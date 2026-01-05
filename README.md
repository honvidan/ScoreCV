# ScoreCV

**ScoreCV** is an automated CV screening and matching tool built with NLP techniques. It's designed to help HR professionals quickly rank multiple candidates against a specific job description.

This project was developed to demonstrate fundamental concepts in Natural Language Processing (NLP) and how they can be applied to practical HR tasks.

## Features

-   **Multiple CV Uploads:** Upload one or more CVs (PDF, DOCX, TXT) to be scored against a single job description.
-   **Automated Scoring:** The system uses TF-IDF and Cosine Similarity to calculate a match score for each CV.
-   **CV Classification:** Automatically predicts a job category for each uploaded CV (e.g., "Software Engineer").
-   **Ranked Candidate Results:** View a ranked table of all processed CVs, sorted from most to least relevant, with their corresponding match scores and predicted categories.

## Tech Stack

-   **Backend:** Python 3.10+, Flask
-   **Frontend:** Python 3.10+, Streamlit, Pandas
-   **NLP:** NLTK, scikit-learn
-   **File Parsing:** PyPDF2, python-docx

## How It Works

1.  **File Upload:** The user uploads multiple CVs and a single job description.
2.  **Iterative Analysis:** The application iterates through each CV. For each one, it performs the following steps:
    a. **Text Extraction:** Extracts raw text from the CV and the job description file.
    b. **CV Classification:** Predicts a job category for the CV based on keyword matching.
    c. **Text Cleaning:** Cleans and preprocesses the text from both documents (lemmatization, stop-word removal, etc.).
    d. **Vectorization:** Converts the cleaned text into numerical TF-IDF vectors.
    e. **Similarity Matching:** Calculates the Cosine Similarity between the job description vector and the CV vector to get a match score.
3.  **Displaying Results:** All results are collected and displayed in a single table, ranked by match score, allowing for easy comparison of candidates.

## Setup and Usage

### Prerequisites

-   Python 3.10 or higher
-   `pip` for package installation

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ScoreCV
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1.  **Launch Backend app:**
    ```bash
    python -m backend.main
    ```

2.  **Launch Frontend app:**
    ```bash
    streamlit run ./frontend/app.py
    ```

3.  **Use the application:**
    -   Your browser should open with the ScoreCV interface.
    -   Upload one or more CVs in PDF, DOCX, or TXT format.
    -   Upload a single job description in PDF, DOCX, or TXT format.
    -   Click the "Analyze Documents" button to see the ranked results.

## Project Structure

```
ScoreCV/
├── backend/
│   ├── __init__.py
│   ├── main.py          # Main application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── nlp.py       # NLP preprocessing functions
│   │   └── parser.py    # File parsing and text extraction
│   └── routes/
│       ├── __init__.py
│       └── matching.py  # API routes for matching and classification
├── frontend/
│   ├── app.py           # The main Streamlit application
├── requirements.txt     # Project dependencies
└── README.md            # This file
```