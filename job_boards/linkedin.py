import json
from pathlib import Path
# TODO: Add actual linkedin fetch

def fetch_linkedin_posts(job_title: str, city: str):

    with open(Path.cwd() / "data/dummy_posts.json") as f:
        job_posts = json.load(f)

    return job_posts