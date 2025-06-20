from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Dict, List

CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)
RESULTS_DIR = Path.cwd() / "data/results"
RESULTS_DIR.mkdir(exist_ok=True)

def evaluate_scores(job_postings: Dict, scores: List[float]) -> None:
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(zip(scores, job_postings["jobs"]))
    top5_jobs = sorted_jobs[:5]
    bottom_jobs = sorted_jobs[5:]
    if bottom_jobs:
        job_cache = [x[1] for x in bottom_jobs]
        # TODO: Should put the score in here too
        job_cache = {"job_cache": job_cache}
        with open(CACHE_DIR / f"job_cache_{dt_string}.json", "w") as f:
            json.dump(job_cache, f, indent=4)
    good_jobs = []
    for score, job in top5_jobs:
        print(job["company"], job["title"], score)
        job["score"] = score
        good_jobs.append(job)
    good_jobs = {"best_matches": good_jobs}
    with open(RESULTS_DIR / f"good_jobs_{dt_string}.json", "w") as f:
        json.dump(good_jobs, f, indent=4)