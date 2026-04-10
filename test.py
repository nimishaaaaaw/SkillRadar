from app.nlp_engine import get_match_score, get_skill_analysis
from app.resume_scorer import get_resume_score

resume = """
Python developer with experience in Flask, FastAPI, Docker, MySQL.
Built REST APIs, deployed on AWS EC2. Familiar with scikit-learn and pandas.
"""

jd = """
Looking for a Python developer with Flask or FastAPI experience.
Should know Docker, databases like MySQL or PostgreSQL, and basic ML libraries.
AWS knowledge is a plus.
"""

print("Match Score:", get_match_score(resume, jd))
print("Skills:", get_skill_analysis(resume, jd))
print("Resume Score:", get_resume_score(resume))