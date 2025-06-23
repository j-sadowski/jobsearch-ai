from datetime import datetime, timezone
import json
from pathlib import Path
from typing import List

from datamodels.models import JobInfo



CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)

def evaluate_scores(job_scores: List[JobInfo], top_n=5) -> None:
    """
    Evaluates and displays the top job matches based on their suitability scores.

    This function sorts the provided list of JobInfo objects by their score in descending order,
    prints the top N jobs (including company, job title, score, and explanation), and saves all
    scored jobs to a timestamped JSON cache file for later review.

    Args:
        job_scores (List[JobInfo]): A list of JobInfo objects, each with a score and explanation.
        top_n (int, optional): The number of top jobs to display. Defaults to 5.

    Returns:
        None
    """
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(job_scores, key=lambda x: x.score, reverse=True)

    for job in sorted_jobs[:top_n]:
        print(job.company, job.job_title, job.score, job.explanation)
    jobs_d = {"query_date": dt_string, "jobs": [x.model_dump() for x in sorted_jobs]}
    with open(CACHE_DIR / f"jobs_{dt_string}.json", "w") as f:
        json.dump(jobs_d, f, indent=4)