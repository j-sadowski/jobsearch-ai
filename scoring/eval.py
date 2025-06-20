from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List

CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)
RESULTS_DIR = Path.cwd() / "data/results"
RESULTS_DIR.mkdir(exist_ok=True)

def evaluate_scores(job_scores: List[Dict], top_n=5) -> None:
    """
    """
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(job_scores, key=lambda x: x["score"])
    top_jobs = sorted_jobs[:top_n]
    bottom_jobs = sorted_jobs[top_n:]
    if bottom_jobs:
        job_cache = {"job_cache": bottom_jobs}
        with open(CACHE_DIR / f"job_cache_{dt_string}.json", "w") as f:
            json.dump(job_cache, f, indent=4)

    for job in top_jobs:
        print(job["company"], job["title"], job["score"], job["explanation"])
    good_jobs = {"best_matches": top_jobs}
    with open(RESULTS_DIR / f"good_jobs_{dt_string}.json", "w") as f:
        json.dump(good_jobs, f, indent=4)