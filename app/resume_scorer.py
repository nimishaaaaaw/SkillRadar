import re


# Action verbs that signal strong, results-driven writing
ACTION_VERBS = [
    "built", "designed", "developed", "implemented", "created", "architected",
    "engineered", "deployed", "optimised", "optimized", "automated", "integrated",
    "built", "launched", "delivered", "reduced", "improved", "increased",
    "managed", "led", "collaborated", "contributed", "configured", "containerised",
    "containerized", "migrated", "refactored", "debugged", "tested", "documented",
    "analysed", "analyzed", "researched", "trained", "fine-tuned", "published",
    "established", "maintained", "monitored", "secured", "scaled", "streamlined",
    "generated", "extracted", "processed", "visualised", "visualized", "modelled",
    "modeled", "predicted", "classified", "clustered", "evaluated", "benchmarked",
]

# Sections a strong resume should have
EXPECTED_SECTIONS = [
    "experience", "education", "skills", "projects",
    "certifications", "summary", "objective",
]


def check_length(text):
    """
    Score based on word count.
    Ideal resume: 300–700 words.
    Returns score out of 20 and a feedback string.
    """
    word_count = len(text.split())

    if 300 <= word_count <= 700:
        return 20, f"Good length ({word_count} words). Fits a single page."
    elif 200 <= word_count < 300:
        return 13, f"Slightly short ({word_count} words). Consider expanding project descriptions."
    elif 700 < word_count <= 900:
        return 13, f"Slightly long ({word_count} words). Try trimming to under 700 words."
    elif word_count < 200:
        return 5, f"Too short ({word_count} words). Add more detail to projects and experience."
    else:
        return 5, f"Too long ({word_count} words). Aim for a single page — under 700 words."


def check_sections(text):
    """
    Score based on presence of expected resume sections.
    Returns score out of 20 and feedback string.
    """
    text_lower = text.lower()
    found = [s for s in EXPECTED_SECTIONS if s in text_lower]
    missing = [s for s in EXPECTED_SECTIONS if s not in text_lower]

    score = round((len(found) / len(EXPECTED_SECTIONS)) * 20)

    if missing:
        feedback = f"Found sections: {', '.join(found)}. Consider adding: {', '.join(missing)}."
    else:
        feedback = "All key sections detected."

    return score, feedback


def check_action_verbs(text):
    """
    Score based on usage of action verbs.
    Returns score out of 20 and feedback string.
    """
    text_lower = text.lower()
    found_verbs = []

    for verb in ACTION_VERBS:
        pattern = r'\b' + re.escape(verb) + r'\b'
        if re.search(pattern, text_lower):
            found_verbs.append(verb)

    # Remove duplicates
    found_verbs = list(set(found_verbs))
    count = len(found_verbs)

    if count >= 8:
        score = 20
        feedback = f"Strong use of action verbs ({count} found). Great."
    elif count >= 5:
        score = 14
        feedback = f"Decent action verb usage ({count} found). Try adding more variety."
    elif count >= 2:
        score = 8
        feedback = f"Low action verb count ({count} found). Use verbs like: built, designed, deployed."
    else:
        score = 2
        feedback = "Almost no action verbs found. Start bullet points with verbs like: built, designed, implemented."

    return score, feedback


def check_quantification(text):
    """
    Score based on presence of numbers and metrics.
    Looks for patterns like: 90%, 3x, 10+ users, $500K, 300ms.
    Returns score out of 20 and feedback string.
    """
    patterns = [
        r'\d+%',           # percentages: 90%, 30%
        r'\d+x\b',         # multipliers: 3x, 10x
        r'\d+\+',          # approximations: 10+, 500+
        r'\$[\d,]+',       # dollar amounts: $500K
        r'\d+ms\b',        # milliseconds: 300ms
        r'\d+\s*users',    # user counts: 10 users
        r'\d+\s*teams?',   # team sizes: 4-person team
        r'\d+\s*endpoint', # endpoints: 13 endpoints
        r'\d+\s*sprint',   # sprints: 3 sprints
        r'\d+\s*table',    # tables: 5 tables
        r'\b\d{3,}\b',     # any large number: 522000, 300
    ]

    matches = []
    for pattern in patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        matches.extend(found)

    count = len(set(matches))

    if count >= 6:
        score = 20
        feedback = f"Well quantified ({count} metrics found). Numbers make bullets concrete."
    elif count >= 3:
        score = 13
        feedback = f"Some quantification ({count} metrics found). Add more numbers where possible."
    elif count >= 1:
        score = 7
        feedback = f"Minimal quantification ({count} metric found). Try to add percentages, counts, or time values."
    else:
        score = 0
        feedback = "No metrics found. Add numbers — e.g. response times, user counts, dataset sizes."

    return score, feedback


def check_contact_info(text):
    """
    Score based on presence of contact details.
    Returns score out of 20 and feedback string.
    """
    score = 0
    feedback_parts = []

    # Email
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        score += 5
    else:
        feedback_parts.append("email address missing")

    # Phone
    if re.search(r'[\+\d][\d\s\-\(\)]{7,}', text):
        score += 5
    else:
        feedback_parts.append("phone number missing")

    # LinkedIn
    if 'linkedin' in text.lower():
        score += 5
    else:
        feedback_parts.append("LinkedIn profile missing")

    # GitHub
    if 'github' in text.lower():
        score += 5
    else:
        feedback_parts.append("GitHub profile missing")

    if not feedback_parts:
        feedback = "All contact details present — email, phone, LinkedIn, GitHub."
    else:
        feedback = f"Missing: {', '.join(feedback_parts)}."

    return score, feedback


def get_resume_score(resume_text):
    """
    Master function — runs all 5 checks and returns
    total score, breakdown, and per-check feedback.
    """
    length_score, length_feedback = check_length(resume_text)
    sections_score, sections_feedback = check_sections(resume_text)
    verbs_score, verbs_feedback = check_action_verbs(resume_text)
    quant_score, quant_feedback = check_quantification(resume_text)
    contact_score, contact_feedback = check_contact_info(resume_text)

    total = length_score + sections_score + verbs_score + quant_score + contact_score

    breakdown = [
        {
            "label": "Resume Length",
            "score": length_score,
            "max": 20,
            "feedback": length_feedback
        },
        {
            "label": "Key Sections",
            "score": sections_score,
            "max": 20,
            "feedback": sections_feedback
        },
        {
            "label": "Action Verbs",
            "score": verbs_score,
            "max": 20,
            "feedback": verbs_feedback
        },
        {
            "label": "Quantification",
            "score": quant_score,
            "max": 20,
            "feedback": quant_feedback
        },
        {
            "label": "Contact Info",
            "score": contact_score,
            "max": 20,
            "feedback": contact_feedback
        },
    ]

    return {
        "total": total,
        "max": 100,
        "breakdown": breakdown
    }