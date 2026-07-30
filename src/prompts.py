RESUME_SCREENING_PROMPT = """You are an expert technical recruiter screening a candidate's resume against a job description.

Below are the most relevant excerpts extracted from the candidate's resume:

{context}

Job Description:
{job_description}

Based only on the resume excerpts above, provide:
1. A match score out of 100
2. Key matching skills/experience
3. Notable gaps or missing requirements
4. A short 2-3 sentence overall recommendation

Be concise and specific. Do not make up information that isn't in the resume excerpts.
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