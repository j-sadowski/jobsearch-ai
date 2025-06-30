import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from pprint import pprint
from typing import List

from datamodels.models import JobInfo
from scoring.oa_models import score_resume

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

CACHE_DIR = Path.cwd() / "data/cache"
CACHE_DIR.mkdir(exist_ok=True)

def run_eval(resume: str, jobs_formatted: List[JobInfo], num_iter=5):
    dt_string = datetime.now(timezone.utc).strftime(format="%Y%m%d-%H%M%S")
    all_outputs = []
    for i, job in enumerate(jobs_formatted):
        result_dict = {
            "original_score": job.score,
            "original_explanation": job.explanation,
            "new_scores": [],
            "new_explanations": [],
        }
        for _ in range(num_iter):
            output = score_resume(resume_text=resume, job_description=job.description)
            result_dict["new_scores"].append(output.score)
            result_dict["new_explanations"].append(output.explanation)
        print("")
        print(f"Result {i}")
        pprint(result_dict)
        all_outputs.append(result_dict)
    output_file = CACHE_DIR / f"eval_results_{dt_string}.json"
    with open(output_file, "w") as f:
        json.dump(all_outputs, f, indent=4)
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM based job searches given a prompt")
    parser.add_argument("-r", "--resume_path", type=Path, help="Path to local resume, currently only .txt format", required=True)
    parser.add_argument("-c", "--cache_path", type=Path, help="The cache to test against", required=True)
    parser.add_argument("-n", "--num_iters", type=int, default=5)
    args = parser.parse_args()

    logger.info(f"Reading resume from {args.resume_path}")
    with open(args.resume_path) as f:
        resume = f.read()
    with open(args.cache_path) as f:
        cache_data = json.load(f)
    jobs_formatted = [JobInfo.model_validate(x) for x in cache_data["jobs"]]

    run_eval(resume, jobs_formatted, num_iter=args.num_iters)
