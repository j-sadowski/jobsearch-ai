import logging
from typing import List

from apify_client import ApifyClient

from config import APIFY_API_KEY
from datamodels.models import JobInfo, WorkflowReqs


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

client = ApifyClient(token=APIFY_API_KEY)


def fetch_posts(search_data: WorkflowReqs) -> List[JobInfo]:
    """
    Fetches job postings using APIFY Jobs Scraper API.

    This function queries APIFY for job postings that match the specified job title and city.
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
        "keywords": search_data.keywords,
        "limit": search_data.limit,
        "location": search_data.city,
    }
    if search_data.hybrid:
        run_input["remote"] = "hybrid"
    run = client.actor("apimaestro/linkedin-jobs-scraper-api").call(run_input=run_input)
    
    jobs = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        try:
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
        except Exception as e:
            logger.error(f"Unable to unpack returned item: {e}")
            continue
    return jobs