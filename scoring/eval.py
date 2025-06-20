from datetime import datetime, timezone
import json
from pathlib import Path
from typing import List

from datamodels.models import JobInfo



CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)
RESULTS_DIR = Path.cwd() / "data/results"
RESULTS_DIR.mkdir(exist_ok=True)

def evaluate_scores(job_scores: List[JobInfo], top_n=5) -> None:
    """
    """
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(job_scores, key=lambda x: x.score, reverse=True)
    top_jobs = sorted_jobs[:top_n]
    bottom_jobs = sorted_jobs[top_n:]
    if bottom_jobs:
        job_cache = {"job_cache": [x.model_dump() for x in bottom_jobs]}
        with open(CACHE_DIR / f"job_cache_{dt_string}.json", "w") as f:
            json.dump(job_cache, f, indent=4)

    for job in top_jobs:
        print(job.company, job.job_title, job.score, job.explanation)
    good_jobs = {"best_matches": [x.model_dump() for x in top_jobs]}
    with open(RESULTS_DIR / f"good_jobs_{dt_string}.json", "w") as f:
        json.dump(good_jobs, f, indent=4)