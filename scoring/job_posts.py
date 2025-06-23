import logging
from typing import List

from .oa_models import score_resume
from datamodels.models import JobInfo


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def score_job_posts(resume: str, job_postings: List[JobInfo]) -> List[JobInfo]:
    """
    Scores a list of job postings against a candidate's resume using an LLM.

    For each job posting, this function evaluates how well the provided resume matches
    the job description by calling the score_resume function. It updates each JobInfo object
    with a suitability score and an explanation. If an error occurs during scoring, the job's
    score is set to -1.

    Args:
        resume (str): The plain text content of the candidate's resume.
        job_postings (List[JobInfo]): A list of JobInfo objects representing job postings to score.

    Returns:
        List[JobInfo]: The input list of JobInfo objects, each updated with a score and explanation.
    """
    scores = []
    for job in job_postings:
        job_score = score_resume(resume, job.description)
        job.score = job_score.score
        job.explanation = job_score.explanation
        scores.append(job)
    return scores