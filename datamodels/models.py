from typing import Optional
from pydantic import BaseModel, Field

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
    score: Optional[float] = Field("Assigned score by LLM")
    explanation: Optional[str] = Field("Short explanation as to why the score was given") 

