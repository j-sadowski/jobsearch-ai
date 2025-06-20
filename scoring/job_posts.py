import logging
from typing import List

from .oa_models import score_resume
from ..job_boards.linkedin import JobInfo

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def extract_job_score(job_score):
    return job_score

def score_job_posts(resume: str, job_postings: List[JobInfo]) -> List[float]:
    """
    There is a 1:1 matching of score against N job_postings.
    Errored jobs return a value of -1.
    """

    scores = []
    for job in job_postings:
        job_score = score_resume(resume, job.description)
        job.score = job_score.score
        job.explanation = job_score.explanation
        scores.append(job)
    return scores