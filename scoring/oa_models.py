import logging
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

load_dotenv()

model = "gpt-4.1-nano-2025-04-14" # Smallest, cheapest for prototyping
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



class ResumeDigest(BaseModel):
    """First LLM call: Summarize the resume"""
    summary: str = Field(description="Summary of the input resume")

class JDScore(BaseModel):
    """Second LLM call score the JD against the resume"""
    score: float = Field(description="Resume suitability score")
    explanation: str = Field(description="Explanation of suitability score")

def resume_summarizer(resume: str) -> ResumeDigest:
    """
    Digest resume to keep the important bits for the for loop analysis

    Leaving this in for reference, but it makes the results worse. Probably needs to be replaced with
    a tokenization step or something.
    """
    logger.info("Starting resume summarizer")
    

    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Summarize the provided resume, extract the important key words and phrases.",
            },
            {"role": "user", "content": resume},
        ],
        response_format=ResumeDigest,
    )
    result = completion.choices[0].message.parsed
    logger.info("Summary complete!")
    print(result.summary)
    return result


def score_resume(resume_text: str, job_description: str) -> JDScore:
    """
    """
    logger.info("Starting resume scorer")
    system_prompt = (
        "You are an expert resume evaluator. Your task is to score a resume's suitability "
        "for a given job description on a scale of 0 to 10. "
        "A score of 10 indicates a perfect fit, and 0 indicates no fit. "
        "Consider all aspects: skills, experience, qualifications, and alignment with the role's responsibilities. "
        "Provide the numerical score as an float and a short explanation."
    )

    user_prompt = (
        f"Resume:\n---\n{resume_text}\n---\n\n"
        f"Job Description:\n---\n{job_description}\n---\n\n"
        "Score this resume against the job description (0-10):"
    )

    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.0,
        response_format=JDScore
    )
    logger.info("Score complete!")
    result = response.choices[0].message.parsed
    print(result)
    return result