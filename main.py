import argparse
import logging
from pathlib import Path

from job_boards.linkedin import fetch_linkedin_posts
from scoring.job_posts import score_job_posts
from scoring.eval import evaluate_scores

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def run_workflow(resume: str, job_title: str, city: str) -> None:
    """
    1. Fetch linkedin job postings that match job_title and city (or remote)
    2. Compare each job posting against the resume, apply a score and a reason
    3. Sort to top 5 jobs, then evaluate jobs that were not included and why
    """
    job_postings = fetch_linkedin_posts(job_title, city)
    scores = score_job_posts(resume, job_postings)
    evaluate_scores(job_postings, scores)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM based job searches given a prompt")
    parser.add_argument("-r", "--resume_path", type=Path, help="Path to local resume, currently only .txt format", required=True)
    parser.add_argument("-j", "--job_title", type=str, help="The job title to search for", required=True)
    parser.add_argument("-c", "--city", type=str, default="Austin, TX")
    args = parser.parse_args()

    logger.info(f"Reading resume from {args.resume_path}")
    with open(args.resume_path) as f:
        resume = f.read()
    logger.info(f"Got job search details looking for {args.job_title} jobs in {args.city}")

    run_workflow(resume, args.job_title, args.city)
