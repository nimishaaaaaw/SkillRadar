import os
import requests
import json


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.1-8b-instant"


def get_groq_key():
    return os.environ.get("GROQ_API_KEY", "")


def get_ai_suggestions(missing_skills, missing_keywords, jd_text, match_score):
    """
    Call Groq LLaMA to generate specific, actionable resume improvement
    suggestions based on the gap analysis results.
    Returns a list of 4-5 suggestion strings.
    """

    missing_skills_str = ', '.join(missing_skills[:10]) if missing_skills else "none identified"
    missing_keywords_str = ', '.join(missing_keywords[:10]) if missing_keywords else "none identified"

    prompt = f"""You are a professional resume coach. A candidate's resume was analysed against a job description.

Match Score: {match_score}%
Missing Tech Skills: {missing_skills_str}
Missing Keywords: {missing_keywords_str}

Job Description Summary:
{jd_text[:800]}

Give exactly 4 specific, actionable suggestions to improve the resume for this role.
Each suggestion must:
- Be one sentence only
- Be concrete and specific, not generic
- Reference actual missing skills or keywords where possible
- Start with an action verb

Return ONLY a JSON array of 4 strings. No explanation, no preamble, no markdown.
Example format: ["suggestion 1", "suggestion 2", "suggestion 3", "suggestion 4"]"""

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {get_groq_key()}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 400
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()

            # Strip markdown code fences if present
            content = content.replace("```json", "").replace("```", "").strip()

            suggestions = json.loads(content)
            if isinstance(suggestions, list):
                return suggestions[:5]
            return ["Could not parse suggestions. Please try again."]

        else:
            print(f"Groq API error: {response.status_code} — {response.text}")
            return ["AI suggestions unavailable. Check your API key."]

    except json.JSONDecodeError:
        return ["Could not parse AI response. Please try again."]
    except requests.exceptions.Timeout:
        return ["AI request timed out. Please try again."]
    except Exception as e:
        print(f"AI service error: {e}")
        return ["AI suggestions temporarily unavailable."]