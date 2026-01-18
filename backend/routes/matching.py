from flask import Blueprint, jsonify, request
from core.parser import extract_text
from core.nlp import preprocess_text, calculate_cosine_similarity

matching_bp = Blueprint('matching', __name__)

# Job categories for CV classification
JOB_CATEGORIES = {
    "Software Engineer": ["python", "java", "backend", "frontend", "developer", "engineer"],
    "Data Scientist": ["machine", "learning", "data", "analysis", "statistic", "analytics"],
    "Product Manager": ["product", "roadmap", "strategy", "agile", "manager"]
}

@matching_bp.route('/classify_cv_file', methods=['POST'])
def classify_cv_file():
    """Classify a CV file into a job category based on keyword matching."""
    if 'cv_file' not in request.files:
        return jsonify({"error": "No CV file provided"}), 400
    
    cv_file = request.files['cv_file']
    if cv_file.filename == '':
        return jsonify({"error": "No selected CV file"}), 400
    
    try:
        cv_text = extract_text(cv_file.stream, cv_file.mimetype)
        if not cv_text:
            return jsonify({"error": f"Could not extract text from {cv_file.filename}"}), 400

        processed_cv_text = preprocess_text(cv_text)
        if not processed_cv_text:
            return jsonify({"error": "Text preprocessing resulted in empty content"}), 400
        
        # Calculate scores for each category
        scores = {cat: 0 for cat in JOB_CATEGORIES}
        text_to_search = processed_cv_text.split()
        
        for cat, keywords in JOB_CATEGORIES.items():
            for keyword in keywords:
                if keyword in text_to_search:
                    scores[cat] += 1
        
        predicted_category = max(scores, key=scores.get) if any(scores.values()) else "Unknown"
        
        return jsonify({"category": predicted_category})
    except Exception as e:
        return jsonify({"error": f"An error occurred during classification: {str(e)}"}), 500

@matching_bp.route('/match_cv_jd_files', methods=['POST'])
def match_cv_jd_files():
    """Calculate match score between a CV and job description using NLP pipeline."""
    if 'cv_file' not in request.files or 'jd_file' not in request.files:
        return jsonify({"error": "Both CV and JD files are required"}), 400
    
    cv_file = request.files['cv_file']
    jd_file = request.files['jd_file']

    if cv_file.filename == '' or jd_file.filename == '':
        return jsonify({"error": "One or both files not selected"}), 400

    try:
        cv_text = extract_text(cv_file.stream, cv_file.mimetype)
        jd_text = extract_text(jd_file.stream, jd_file.mimetype)
        
        if not cv_text or not jd_text:
            return jsonify({"error": "Could not extract text from one or both files"}), 400

        # Use the NLP pipeline to calculate similarity score (0-100%)
        match_score = calculate_cosine_similarity(cv_text, jd_text)
        
        return jsonify({"match_score": match_score})
    except Exception as e:
        return jsonify({"error": f"An error occurred during matching: {str(e)}"}), 500
