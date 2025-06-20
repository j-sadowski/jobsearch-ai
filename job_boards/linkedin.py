import json
from pathlib import Path
# TODO: Add actual linkedin fetch

def fetch_linkedin_posts(job_title: str, city: str):

    with open(Path.cwd() / "job_boards/dummy_posts.json") as f:
        job_posts = json.load(f)

    return job_posts