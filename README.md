# ScoreCV

**ScoreCV** is an automated CV screening and matching tool built with basic NLP techniques. It's designed to help HR professionals quickly identify the most relevant candidates for a job by scoring and ranking CVs against a given job description.

This project was developed as part of the "Python for Engineering" course to demonstrate fundamental concepts in Natural Language Processing (NLP).

## Features

-   **Job Description Input:** Paste a job description into a text area.
-   **Multiple CV Uploads:** Upload one or more CVs in PDF format.
-   **Automated Scoring:** The system uses TF-IDF and Cosine Similarity to calculate a match score for each CV.
-   **Ranked Results:** View a ranked list of CVs, from most to least relevant, with their corresponding match scores.

## Tech Stack

-   **Backend:** Python 3.10+, Flask
-   **Frontend:** Python 3.10+, Streamlit
-   **NLP:** NLTK, scikit-learn
-   **PDF Parsing:** PyPDF2

## How It Works

1.  **Text Extraction:** The tool first extracts raw text from the uploaded PDF CVs.
2.  **Text Cleaning:** Both the job description and the CV text are cleaned and preprocessed. This involves:
    -   Converting text to lowercase.
    -   Removing punctuation and special characters.
    -   Tokenizing the text into individual words.
    -   Removing common English "stop words" (e.g., "the", "a", "in").
    -   Lemmatizing words to their root form (e.g., "running" becomes "run").
3.  **Vectorization:** The cleaned text is converted into numerical vectors using the TF-IDF (Term Frequency-Inverse Document Frequency) algorithm. This technique highlights words that are important to a document within a collection of documents.
4.  **Similarity Matching:** The system calculates the Cosine Similarity between the job description vector and each CV vector. The resulting score (from 0 to 100) represents how well the CV matches the job description.
5.  **Displaying Results:** The CVs are ranked by their scores and displayed in a clean, easy-to-read format.

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
    python ./backend/api.py
    ```

1.  **Launch Frontend app:**
    ```bash
    streamlit run ./frontend/app.py
    ```

2.  **Use the application:**
    -   Your browser should open with the ScoreCV interface.
    -   Paste the job description into the text area.
    -   Upload one or more CVs in PDF format.
    -   Click the "Generate Scores" button to see the results.

## Project Structure

```
ScoreCV/
├── backend/
│   ├── api.py
├── frontend/
│   ├── app.py           # The main Streamlit application
├── requirements.txt     # Project dependencies
└── README.md            # This file
```