import os
from typing import List

from dotenv import load_dotenv
from apify_client import ApifyClient

from datamodels.models import JobInfo

load_dotenv()

client = ApifyClient(token=os.getenv("APIFY_API_KEY"))


def fetch_linkedin_posts(job_title: str, city: str, limit=5, hybrid=False) -> List[JobInfo]:
    """
    Fetches job postings from LinkedIn using the Apify LinkedIn Jobs Scraper API.

    This function queries LinkedIn for job postings that match the specified job title and city.
    It returns a list of JobInfo objects containing details about each job. Optionally, it can filter
    for hybrid/remote jobs.

    Args:
        job_title (str): The job title to search for.
        city (str): The city to search for jobs in.
        limit (int, optional): The maximum number of job postings to fetch. Defaults to 5.
        hybrid (bool, optional): If True, only fetch hybrid/remote jobs. Defaults to False.

    Returns:
        List[JobInfo]: A list of JobInfo objects representing the fetched job postings.
    """
    run_input = {
        "date_posted": "week", # only show results from last week
        "keywords": job_title,
        "limit": limit,
        "location": city,
    }
    if hybrid:
        run_input["remote"] = "hybrid"
    run = client.actor("apimaestro/linkedin-jobs-scraper-api").call(run_input=run_input)
    
    jobs = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        jobs.append(
            JobInfo(
                company=item.get("company", "Not Specified"),
                company_url=item.get("company_url", "Not Specified"),
                description=item.get("description", "Not Specified"),
                is_verified=item.get("is_verified", False),
                job_title=item.get("job_title", "Not Specified"),
                job_url=item.get("job_url", "Not Specified"),
                location=item.get("location", "Not Specified"),
                posted_at=item.get("posted_at", "Not Specified"),
                salary=item.get("salary", "Not Specified"),
                work_type=item.get("work_type", "Not Specified")\
            )
        )
    return jobs