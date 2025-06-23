from datetime import datetime, timezone
import json
from pathlib import Path
from typing import List

from datamodels.models import JobInfo



CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)

def evaluate_scores(job_scores: List[JobInfo], top_n=5) -> None:
    """
    """
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(job_scores, key=lambda x: x.score, reverse=True)

    for job in sorted_jobs[:top_n]:
        print(job.company, job.job_title, job.score, job.explanation)
    good_jobs = {"query_date": dt_string, "jobs": [x.model_dump() for x in sorted_jobs]}
    with open(CACHE_DIR / f"jobs_{dt_string}.json", "w") as f:
        json.dump(good_jobs, f, indent=4)