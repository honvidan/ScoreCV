from flask import Blueprint, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core.parser import extract_text
from core.nlp import preprocess_text

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/classify_cv_file', methods=['POST'])
def classify_cv_file():
    if 'cv_file' not in request.files:
        return jsonify({"error": "No CV file provided"}), 400
    
    cv_file = request.files['cv_file']
    if cv_file.filename == '':
        return jsonify({"error": "No selected CV file"}), 400
    
    cv_text = extract_text(cv_file.stream, cv_file.mimetype)
    if not cv_text:
        return jsonify({"error": f"Could not extract text from {cv_file.filename}"}), 400

    processed_cv_text = preprocess_text(cv_text)
    
    categories = {
        "Software Engineer": ["python", "java", "backend", "frontend", "developer", "engineer"],
        "Data Scientist": ["machine", "learning", "data", "analysis", "statistic", "analytics"],
        "Product Manager": ["product", "roadmap", "strategy", "agile", "manager"]
    }
    
    scores = {cat: 0 for cat in categories}
    text_to_search = processed_cv_text.split()
    for cat, keywords in categories.items():
        for keyword in keywords:
            if keyword in text_to_search:
                scores[cat] += 1
    
    predicted_category = max(scores, key=scores.get) if any(scores.values()) else "Unknown"
    
    return jsonify({"category": predicted_category})

@matching_bp.route('/match_cv_jd_files', methods=['POST'])
def match_cv_jd_files():
    if 'cv_file' not in request.files or 'jd_file' not in request.files:
        return jsonify({"error": "Both CV and JD files are required"}), 400
    
    cv_file = request.files['cv_file']
    jd_file = request.files['jd_file']

    if cv_file.filename == '' or jd_file.filename == '':
        return jsonify({"error": "One or both files not selected"}), 400

    cv_text = extract_text(cv_file.stream, cv_file.mimetype)
    jd_text = extract_text(jd_file.stream, jd_file.mimetype)
    
    if not cv_text or not jd_text:
        return jsonify({"error": "Could not extract text from one or both files"}), 400
        
    processed_cv = preprocess_text(cv_text)
    processed_jd = preprocess_text(jd_text)
    
    if not processed_cv or not processed_jd:
        return jsonify({"error": "Text preprocessing resulted in empty content"}), 400

    documents = [processed_cv, processed_jd]
    
    tfidf_vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    except ValueError:
        return jsonify({"error": "Could not vectorize documents, possibly due to empty vocabulary."}), 400

    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    match_score = float(cosine_sim[0][0])
    
    return jsonify({"match_score": match_score})
