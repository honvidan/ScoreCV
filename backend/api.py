from flask import Flask, jsonify, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import io

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

@app.route('/classify_cv_file', methods=['POST'])
def classify_cv_file():
    if 'cv_file' not in request.files:
        return jsonify({"error": "No CV file provided"}), 400
    
    cv_file = request.files['cv_file']
    if cv_file.filename == '':
        return jsonify({"error": "No selected CV file"}), 400
    
    cv_text = extract_text_from_pdf(cv_file.stream)
    
    # Simple keyword-based classification
    categories = {
        "Software Engineer": ["python", "java", "backend", "frontend", "developer"],
        "Data Scientist": ["machine learning", "data analysis", "statistics", "analytics"],
        "Product Manager": ["product", "roadmap", "strategy", "agile"]
    }
    
    scores = {cat: 0 for cat in categories}
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in cv_text.lower():
                scores[cat] += 1
    
    if not scores or all(value == 0 for value in scores.values()):
        predicted_category = "Unknown"
    else:
        predicted_category = max(scores, key=scores.get)
    
    return jsonify({"category": predicted_category})

@app.route('/match_cv_jd_files', methods=['POST'])
def match_cv_jd_files():
    if 'cv_file' not in request.files:
        return jsonify({"error": "No CV file provided"}), 400
    if 'jd_file' not in request.files:
        return jsonify({"error": "No JD file provided"}), 400
    
    cv_file = request.files['cv_file']
    jd_file = request.files['jd_file']

    if cv_file.filename == '' or jd_file.filename == '':
        return jsonify({"error": "No selected CV or JD file"}), 400

    cv_text = extract_text_from_pdf(cv_file.stream)
    
    jd_text = ""
    if jd_file.mimetype == 'application/pdf':
        jd_text = extract_text_from_pdf(jd_file.stream)
    else: # Assume text file
        jd_text = jd_file.stream.read().decode('utf-8')
    
    if not cv_text or not jd_text:
        return jsonify({"error": "Could not extract text from one or both files"}), 400
        
    documents = [cv_text, jd_text]
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    match_score = float(cosine_sim[0][0])
    
    return jsonify({"match_score": match_score})

if __name__ == '__main__':
    app.run(port=5000)