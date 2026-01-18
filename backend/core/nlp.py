import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Vietnamese stopwords list (deduplicated)
VIETNAMESE_STOPWORDS = {
    'và', 'của', 'cho', 'với', 'trong', 'là', 'có', 'được', 'một', 'các', 'từ', 'này', 'đó',
    'về', 'sau', 'khi', 'như', 'theo', 'đến', 'nếu', 'mà', 'đã', 'sẽ', 'bị', 'bởi', 'ở',
    'vào', 'ra', 'lên', 'xuống', 'qua', 'lại', 'đây', 'đấy', 'nào', 'đâu', 'sao', 'thế',
    'để', 'vì', 'do', 'nên', 'nhưng', 'hoặc', 'hay', 'thì',
    'cũng', 'rất', 'quá', 'còn', 'chỉ', 'mới', 'đang', 'vừa',
    'cả', 'tất', 'mọi', 'mỗi', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám',
    'chín', 'mười', 'nhiều', 'ít', 'hơn', 'kém', 'bằng', 'không',
    'phải', 'chưa', 'chẳng', 'chả', 'gì', 'ai'
}

# Cache for English stopwords to avoid reloading
_ENGLISH_STOPWORDS = None


def setup_nltk():
    """Download required NLTK data if not present."""
    global _ENGLISH_STOPWORDS
    try:
        _ENGLISH_STOPWORDS = set(stopwords.words('english'))
    except LookupError:
        print("Downloading NLTK stopwords...")
        nltk.download('stopwords')
        _ENGLISH_STOPWORDS = set(stopwords.words('english'))
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt...")
        nltk.download('punkt')


def lowercase_and_remove_punctuation(text):
    """
    Step 1: Convert text to lowercase and remove punctuation.
    
    Args:
        text: Input text string
        
    Returns:
        Text in lowercase without punctuation
    """
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


def tokenize(text):
    """
    Step 2: Tokenization - split text into words.
    
    Args:
        text: Input text string
        
    Returns:
        List of tokens (words)
    """
    if not text:
        return []
    # Use NLTK word tokenizer
    tokens = word_tokenize(text)
    # Filter out non-alphabetic tokens and keep only words
    tokens = [word for word in tokens if word.isalpha()]
    return tokens


def remove_stopwords(tokens):
    """
    Step 3: Remove stopwords (English + Vietnamese).
    
    Args:
        tokens: List of word tokens
        
    Returns:
        List of tokens with stopwords removed
    """
    if not tokens:
        return []
    
    # Use cached English stopwords or fallback
    global _ENGLISH_STOPWORDS
    if _ENGLISH_STOPWORDS is None:
        try:
            _ENGLISH_STOPWORDS = set(stopwords.words('english'))
        except LookupError:
            _ENGLISH_STOPWORDS = set()
    
    # Combine English and Vietnamese stopwords
    all_stopwords = _ENGLISH_STOPWORDS | VIETNAMESE_STOPWORDS
    
    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in all_stopwords]
    return filtered_tokens


def preprocess_text(text):
    """
    Complete NLP preprocessing pipeline:
    1. Lowercase + Remove Punctuation
    2. Tokenization
    3. Stopword Removal (English + Vietnamese)
    
    Args:
        text: Raw input text
        
    Returns:
        Preprocessed text as a string (space-separated tokens)
    """
    if not text:
        return ""
    
    # Step 1: Lowercase + Remove Punctuation
    text = lowercase_and_remove_punctuation(text)
    
    # Step 2: Tokenization
    tokens = tokenize(text)
    
    # Step 3: Stopword Removal
    tokens = remove_stopwords(tokens)
    
    # Return as space-separated string for TF-IDF
    return " ".join(tokens)


def tfidf_vectorize(texts):
    """
    Step 4: TF-IDF Vectorization.
    
    Args:
        texts: List of preprocessed text strings
        
    Returns:
        TF-IDF vectorizer and matrix
    """
    if not texts or not any(texts):
        raise ValueError("Cannot vectorize empty texts")
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    return vectorizer, tfidf_matrix


def calculate_cosine_similarity(text1, text2):
    """
    Complete NLP Pipeline:
    1. Lowercase + Remove Punctuation
    2. Tokenization
    3. Stopword Removal (English + Vietnamese)
    4. TF-IDF Vectorization
    5. Cosine Similarity Calculation
    
    Args:
        text1: First input text
        text2: Second input text
        
    Returns:
        Similarity score as percentage (0-100%)
    """
    if not text1 or not text2:
        return 0.0
    
    # Preprocess both texts
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    # Check if preprocessing resulted in empty texts
    if not processed_text1 or not processed_text2:
        return 0.0
    
    # Step 4: TF-IDF Vectorization
    try:
        vectorizer, tfidf_matrix = tfidf_vectorize([processed_text1, processed_text2])
    except ValueError:
        return 0.0
    
    # Step 5: Cosine Similarity Calculation
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    similarity_score = float(cosine_sim[0][0])
    
    # Convert to percentage (0-100%)
    similarity_percentage = similarity_score * 100
    
    return similarity_percentage
