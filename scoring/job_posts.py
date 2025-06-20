import logging
from typing import Dict, List

from .oa_models import score_resume

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def extract_job_score(job_score):
    return job_score

def score_job_posts(resume: str, job_postings: Dict) -> List[float]:
    """
    There is a 1:1 matching of score against N job_postings.
    Errored jobs return a value of -1.
    """
    # I'm just modifying the job_posting dict in place and throwing it into a list, which seems a bit too clever
    scores = []
    for i, job in enumerate(job_postings["jobs"]):
        job_score = score_resume(resume, job["job_description"])
        job["score"] = job_score.score
        job["explanation"] = job_score.explanation
        scores.append(job)
    return scores