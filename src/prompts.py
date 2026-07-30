RESUME_SCREENING_PROMPT = """You are an expert technical recruiter and ATS (Applicant Tracking System) analyst screening a candidate's resume against a job description.

Below are the most relevant excerpts extracted from the candidate's resume:

{context}

Job Description:
{job_description}

Based only on the resume excerpts above, respond with STRICT JSON ONLY (no markdown, no code fences, no extra text before or after) matching exactly this structure:

{{
  "candidate_summary": "a 2-3 sentence neutral summary of who this candidate is professionally",
  "experience_level": "one of: Entry-level, Junior, Mid-level, Senior, Lead/Principal",
  "match_score": <integer 0-100, how well the resume matches the job description>,
  "ats_score": <integer 0-100, how well the resume is structured/keyword-optimized for automated ATS parsing, independent of job fit>,
  "top_skills": ["most relevant skill 1", "most relevant skill 2", "up to 5 total, ranked by relevance"],
  "matching_skills": ["skill or experience that matches the job description"],
  "missing_skills": ["gap or missing requirement relative to the job description"],
  "interview_questions": ["a targeted interview question to probe a specific gap or claim", "up to 5 total"],
  "hiring_decision": "one of: Strong Match, Consider, Weak Match, Not a Fit",
  "recommendation": "a short 2-3 sentence overall recommendation"
}}

Do not make up information that isn't in the resume excerpts. Return ONLY the JSON object, nothing else.
"""


def build_screening_prompt(context: str, job_description: str) -> str:
    """
    Fills the resume screening prompt template with retrieved context
    and the job description.
    """
    return RESUME_SCREENING_PROMPT.format(
        context=context,
        job_description=job_description
    )