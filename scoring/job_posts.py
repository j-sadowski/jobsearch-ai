import logging
from typing import Dict, List
import numpy as np


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def llm_call_resume(resume):
    return resume[:50]

def llm_call_jobs(job, resume_digest):
    return np.random.randn()

def extract_job_score(job_score):
    return job_score

def score_job_posts(resume: str, job_postings: Dict) -> List[float]:
    """
    There is a 1:1 matching of score against N job_postings.
    Errored jobs return a value of -1.
    """
    resume_digest = llm_call_resume(resume)
    scores = []
    for i, job in enumerate(job_postings):
        try:
            job_score = llm_call_jobs(job, resume_digest)
        except Exception as e:
            logger.error("Failed to run LLM call on job number {i}: {e}")
            scores.append(-1)
            continue
        try: 
            scores.append(extract_job_score(job_score))
        except Exception as e:
            logger.error("Failed to extract job_score from job {i}: {e}")
            scores.append(-1)
    return scores