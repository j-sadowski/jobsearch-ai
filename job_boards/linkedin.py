import os
from typing import List

from dotenv import load_dotenv
from apify_client import ApifyClient
from pydantic import BaseModel, Field


load_dotenv()

client = ApifyClient(token=os.getenv("APIFY_API_KEY"))

# TODO: Move this to a models file
class JobInfo(BaseModel):
    company: str = Field("The company's name")
    company_url: str = Field("LinkedIn Company URL")
    description: str = Field("The job description")
    is_verified: bool = Field("Whether the company has been verified")
    job_title: str = Field("Job Title")
    job_url: str = Field("LinkedIn Job URL")
    location: str = Field("Location")
    work_type: str = Field("OnSite/Remote/Hybrid status")
    posted_at: str = Field("Posting date")
    salary: str = Field("Provided salary information")


def fetch_linkedin_posts(job_title: str, city: str, limit=5) -> List[JobInfo]:
    run_input = {
        "date_posted": "week", # only show results from last week
        "keywords": job_title,
        "limit": limit,
        "location": city,
        "remote": "hybrid"
    }
    run = client.actor("apimaestro/linkedin-jobs-scraper-api").call(run_input=run_input)
    
    jobs = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        jobs.append(JobInfo(
            company=item["company"],
            company_url=item["company_url"],
            description=item["description"],
            is_verified=item["is_verified"],
            job_title=item["job_title"],
            job_url=item["job_url"],
            location=item["location"],
            posted_at=item["posted_at"],
            salary=item["salary"],
            work_type=item["work_type"]
        ))
    return jobs