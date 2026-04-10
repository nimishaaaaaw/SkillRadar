import os
from flask import Blueprint, render_template, request, session
from app.nlp_engine import get_match_score, get_keyword_analysis, get_skill_analysis
from app.resume_scorer import get_resume_score
from app.pdf_utils import extract_text_from_pdf, is_valid_pdf
from app.ai_service import get_ai_suggestions

main = Blueprint('main', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/analyze', methods=['POST'])
def analyze():
    error = None
    resume_text = ""
    jd_text = ""

    # --- Get JD text (always plain text input) ---
    jd_text = request.form.get('jd_text', '').strip()

    # --- Get resume text (PDF upload or plain text) ---
    resume_input_type = request.form.get('resume_input_type', 'text')

    if resume_input_type == 'pdf':
        file = request.files.get('resume_pdf')
        if not file or file.filename == '':
            error = "No PDF file uploaded."
        elif not is_valid_pdf(file):
            error = "Invalid file. Please upload a valid PDF."
        else:
            file.seek(0)
            resume_text = extract_text_from_pdf(file)
            if not resume_text:
                error = "Could not extract text from PDF. Try pasting as text instead."
    else:
        resume_text = request.form.get('resume_text', '').strip()

    # --- Validate inputs ---
    if not error and len(resume_text.split()) < 20:
        error = "Resume text is too short. Please provide more content."
    if not error and len(jd_text.split()) < 10:
        error = "Job description is too short. Please provide more content."

    if error:
        return render_template('index.html', error=error)

    # --- Run all analysis ---
    match_score = get_match_score(resume_text, jd_text)
    keyword_analysis = get_keyword_analysis(resume_text, jd_text)
    skill_analysis = get_skill_analysis(resume_text, jd_text)
    resume_score = get_resume_score(resume_text)

    # --- Get AI suggestions ---
    ai_suggestions = get_ai_suggestions(
        missing_skills=skill_analysis['missing_skills'],
        missing_keywords=keyword_analysis['missing'],
        jd_text=jd_text,
        match_score=match_score
    )

    # --- Store last scan in session ---
    session['last_scan'] = {
        'match_score': match_score,
        'resume_score': resume_score['total'],
        'matched_skills': skill_analysis['matched_skills'],
        'missing_skills': skill_analysis['missing_skills'],
    }

    # --- Score label ---
    if match_score >= 70:
        score_label = "Strong Match"
        score_color = "success"
    elif match_score >= 45:
        score_label = "Moderate Match"
        score_color = "warning"
    else:
        score_label = "Low Match"
        score_color = "danger"

    return render_template(
        'results.html',
        match_score=match_score,
        score_label=score_label,
        score_color=score_color,
        keyword_analysis=keyword_analysis,
        skill_analysis=skill_analysis,
        resume_score=resume_score,
        ai_suggestions=ai_suggestions,
        resume_text=resume_text,
        jd_text=jd_text
    )