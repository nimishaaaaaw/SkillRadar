import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from app.skills_list import TECH_SKILLS

import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)


def clean_text(text):
    """Lowercase, remove punctuation, strip extra whitespace."""
    text = text.lower()
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'[^\w\s\+\#\.]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def remove_stopwords(text):
    """Remove common English stopwords but keep tech terms."""
    stop_words = set(stopwords.words('english'))
    # Keep these — they matter in tech context
    keep_words = {'not', 'no', 'with', 'without', 'and', 'or'}
    stop_words = stop_words - keep_words
    tokens = word_tokenize(text)
    filtered = [w for w in tokens if w not in stop_words]
    return ' '.join(filtered)


def preprocess(text):
    """Full pipeline: clean → remove stopwords."""
    text = clean_text(text)
    text = remove_stopwords(text)
    return text


def get_match_score(resume_text, jd_text):
    """
    Compute TF-IDF cosine similarity between resume and JD.
    Returns a score from 0 to 100.
    """
    resume_clean = preprocess(resume_text)
    jd_clean = preprocess(jd_text)

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(score * 100, 2)
    except Exception:
        return 0.0


def extract_keywords(text, top_n=30):
    """
    Extract top N meaningful keywords from text using TF-IDF scores.
    Returns a list of keyword strings.
    """
    clean = preprocess(text)
    vectorizer = TfidfVectorizer(max_features=top_n, ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([clean])
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
    except Exception:
        return []


def get_keyword_analysis(resume_text, jd_text):
    """
    Compare keywords between resume and JD.
    Returns:
        - matched: keywords in both
        - missing: in JD but not in resume
        - extra: in resume but not in JD
    """
    resume_keywords = set(extract_keywords(resume_text, top_n=40))
    jd_keywords = set(extract_keywords(jd_text, top_n=40))

    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    extra = resume_keywords - jd_keywords

    return {
        'matched': sorted(list(matched)),
        'missing': sorted(list(missing)),
        'extra': sorted(list(extra))
    }


def get_skill_analysis(resume_text, jd_text):
    """
    Cross-reference both texts against the TECH_SKILLS dictionary.
    Returns:
        - matched_skills: tech skills in both resume and JD
        - missing_skills: tech skills in JD but not in resume
        - resume_skills: all tech skills found in resume
        - jd_skills: all tech skills found in JD
    """
    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    resume_skills = set()
    jd_skills = set()

    for skill in TECH_SKILLS:
        # Use word boundary matching to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, resume_lower):
            resume_skills.add(skill)
        if re.search(pattern, jd_lower):
            jd_skills.add(skill)

    matched_skills = resume_skills & jd_skills
    missing_skills = jd_skills - resume_skills

    return {
        'matched_skills': sorted(list(matched_skills)),
        'missing_skills': sorted(list(missing_skills)),
        'resume_skills': sorted(list(resume_skills)),
        'jd_skills': sorted(list(jd_skills))
    }