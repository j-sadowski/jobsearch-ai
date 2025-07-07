import logging
from typing import List

from ollama import chat
from pydantic import BaseModel, Field

from datamodels.models import SearchExtract, WorkflowReqs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

model = "gemma3:1b"

# TODO: Move pydtantic models out of here.
class ResumeDigest(BaseModel):
    """First LLM call: Summarize the resume"""
    summary: str = Field(description="Summary of the input resume")

class JDScore(BaseModel):
    """Second LLM call score the JD against the resume"""
    score: float = Field(description="Resume suitability score")
    explanation: str = Field(description="Explanation of suitability score")

def check_search_prompt(prompt: str) -> SearchExtract:
    logger.info("Checking prompt validity")
    prompt = f"Does the following sentence include job search keywords (job title, city, number of results)?: {prompt}"
    completion = chat(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to validate job search prompts for relevance and data quality.  Your task is to analyze the prompt to determine if it contains keywords indicative of a job search query, a city, and optionally a hybrid status. Respond with a boolean indicating the presence of these elements, a confidence score, and a concise explanation supporting the confidence score"
                },
                {"role": "user", "content": prompt},
            ],
            format=SearchExtract.model_json_schema(),
            options={"temperature": 0.0},
        )
    result = SearchExtract.model_validate_json(completion.message.content)
    logger.info("Check complete!")
    return result

def extract_reqs(prompt: str) -> WorkflowReqs:
    logger.info("Starting prompt extraction")
    completion = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant designed to extract job search information from the prompt.  Your task is to analyze the prompt and extract: a job title, a city, optionally a limit on results and optionally a hybrid status. You are FORBIDDEN from filling in the resume field.",
            },
            {"role": "user", "content": prompt},
        ],
        format=WorkflowReqs.model_json_schema(),
        options={"temperature": 0},
    )
    result = WorkflowReqs.model_validate_json(completion.message.content)
    logger.info("Extraction complete!")
    print(result)
    return result



def resume_summarizer(resume: str) -> ResumeDigest:
    """
    Summarize a resume to extract key keep the important bits for the for loop analysis

    This function sends the provided resume text to an LLM, which returns a concise summary
    highlighting the most important keywords and phrases. The summary is intended to capture
    the core qualifications, skills, and experience from the resume for downstream analysis.
    
    Leaving this in for reference, but it makes the results worse. Probably needs to be replaced with
    a tokenization step or something.

    Args:
        resume (str): The plain text content of the candidate's resume.

    Returns:
        ResumeDigest: An object containing the summarized resume.
    """
    logger.info("Starting resume summarizer")
    

    completion = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Summarize the provided resume, extract the important key words and phrases.",
            },
            {"role": "user", "content": resume},
        ],
        format=ResumeDigest.model_json_schema(),
    )
    result = ResumeDigest.model_validate_json(completion.message.content)
    logger.info("Summary complete!")
    print(result.summary)
    return result


def score_resume(resume_text: str, job_description: str) -> JDScore:
    """
    Evaluates the suitability of a resume for a specific job description.

    Sends both the resume and the job description to LLM, which returns a numerical
    score (0-10) indicating how well the resume matches the job requirements, along with a brief explanation.
    A score of 10 means a perfect fit; 0 means no fit. The evaluation considers skills, experience,
    qualifications, and alignment with the role's responsibilities.

    Args:
        resume_text (str): The plain text content of the candidate's resume.
        job_description (str): The plain text content of the job description.

    Returns:
        JDScore: An object containing the suitability score and an explanation.
    """

    system_prompt = (
        "You are an expert resume evaluator. Your task is to score a resume's suitability "
        "for a given job description on a scale of 0 to 10. "
        "A score of 10 indicates a perfect fit, and 0 indicates no fit. "
        "Be harsh but fair. "
        "Consider all aspects: skills, experience, qualifications, and alignment with the role's responsibilities. "
        "Provide the numerical score as an float and a short explanation (<100 words)."
    )

    user_prompt = (
        f"Resume:\n---\n{resume_text}\n---\n\n"
        f"Job Description:\n---\n{job_description}\n---\n\n"
        "Score this resume against the job description (0-10)."
    )
    try:
        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0},
            format=JDScore.model_json_schema()
        )
        logger.info("Resume scoring successful!")
        result = JDScore.model_validate_json(response.message.content)
    except Exception as e:
        logger.error(f"Failed to score resume: {e}")
        result = JDScore(score=-1, explanation="Comparison failed")
    return result


def summarize_gaps(explanations: List[str]) -> str:
    """
    Analyzes a list of eplanations to extract missing skills or experiences.

    This function sends the provided list of explanations to an LLM, which returns
    a concise bullet-point list of specific skills or experiences that are identified as missing
    or could be improved upon for a higher suitability score. The output is intended to help
    candidates understand what areas of their resume could be strengthened to better match job requirements.

    Args:
        explanations (List[str]): List of rationale strings, each describing aspects of a candidate's profile
                                  in relation to a job description.

    Returns:
        str: A bullet-point list of missing skills or experiences, as identified by the LLM.
    """
    logger.info("Starting gap summarizer")
    
    explanations = [f"Rationale {i}: {x}" for i, x in enumerate(explanations)]    

    system_prompt = (
        "You are an expert at identifying and articulating missing skills and experiences."
        "Your task is to analyze a list of rationales, each describing aspects of a candidate's profile in relation to a job."
        "From these rationales, **extract only the specific skills or experiences that are identified as missing or could be improved upon**"
        "for a higher suitability score. Provide your response as a concise list of bullet points,"
        "with each point clearly stating a missing skill or experience."
        "Do not include any introductory or concluding remarks, just the bullet points."
    )

    user_prompt = (
        f"Analyze the following rationales to identify missing skills or experiences:\n"
        f"{'\n--\n'.join(explanations)}\n--\n\n"
        "List the identified gaps:"
    )
    
    try:
        response = chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": 0},
        )
        logger.info("Gap summarizaton complete")
        result = response["message"]["content"]
    except Exception as e:
        logger.error(f"Failed to identify gaps resume: {e}")
        result = f"Unable to analyze gaps: {e}"
    return result