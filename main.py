import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from typing import List

from datamodels.models import JobInfo
from job_boards.linkedin import fetch_linkedin_posts
from scoring.job_posts import score_job_posts, identify_resume_gaps

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)

def display_output(scores: List[JobInfo], gap_summary: str, top_n=5) -> None:
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    sorted_jobs = sorted(scores, key=lambda x: x.score, reverse=True)

    for job in sorted_jobs[:top_n]:
        print("")
        print(job.company)
        print(f"{job.job_title}, score: {job.score}")
        print(job.explanation)
    jobs_d = {"query_date": dt_string, "jobs": [x.model_dump() for x in sorted_jobs]}
    with open(CACHE_DIR / f"jobs_{dt_string}.json", "w") as f:
        json.dump(jobs_d, f, indent=4)

    print("")
    print("Areas of improvement")
    print(gap_summary)


def run_workflow(resume: str, job_title: str, city: str, limit: int, hybrid:bool) -> None:
    """
    1. Fetch linkedin job postings that match job_title and city (or remote)
    2. Compare each job posting against the resume, apply a score and a reason
    3. Sort to top 5 jobs, then evaluate jobs that were not included and why

    Executes the main workflow for job searching and evaluation.

    Steps:
        1. Fetches LinkedIn job postings that match the specified job title and city.
           If 'hybrid' is True, only hybrid jobs in the search.
        2. Compares each job posting against the provided resume, assigning a score and reason.
        3. Summarize gaps in jobs > 7 that would improve resume
        4. Sorts the job postings by score, prints the top 5, saves all to cache

    Args:
        resume (str): The contents of the user's resume in plain text.
        job_title (str): The job title to search for.
        city (str): The city to search for jobs in. Only the city. Not city, state.
        limit (int): The maximum number of job postings to fetch.
        hybrid (bool): Whether to include hybrid/remote jobs in the search.

    Returns:
        None
    """
    job_postings = fetch_linkedin_posts(job_title, city, limit=limit, hybrid=hybrid)
    if len(job_postings) == 0:
        logger.error("No job posts were returned from fetch. Exiting.")
        return
    scores = score_job_posts(resume, job_postings)
    gap_summary = identify_resume_gaps(scores)
    display_output(scores, gap_summary, top_n=5)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM based job searches given a prompt")
    parser.add_argument("-r", "--resume_path", type=Path, help="Path to local resume, currently only .txt format", required=True)
    parser.add_argument("-j", "--job_title", type=str, help="The job title to search for", required=True)
    parser.add_argument("-c", "--city", type=str, default="Austin")
    parser.add_argument("-l", "--limit", type=int, default=10)
    parser.add_argument("-hyb", "--hybrid", action="store_true")
    args = parser.parse_args()

    logger.info(f"Reading resume from {args.resume_path}")
    with open(args.resume_path) as f:
        resume = f.read()
    logger.info(f"Got job search details looking for {args.job_title} jobs in {args.city}")

    run_workflow(resume, args.job_title, args.city, args.limit, args.hybrid)
