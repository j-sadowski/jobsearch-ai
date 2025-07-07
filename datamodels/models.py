from typing import Optional
from pydantic import BaseModel, Field


class SearchExtract(BaseModel):
    is_valid: bool = Field(description="Whether this text is describing search terms for a job board (keywords, city, limit on number, hybrid status)")
    confidence: float = Field(description="Confidence score that this is a valid search query")
    rationale: str = Field(description="A concise explanation on why the prompt was given this score")

class WorkflowReqs(BaseModel):
    resume: Optional[str] = Field(description="The plain text of a resume")
    keywords: str = Field(description="The job title")
    city: str = Field(description="The city where the job is located. DO NOT include the state")
    limit: Optional[int] = Field(description="The maximum number of items to return", default=20)
    hybrid: Optional[bool] = Field(description="Whether to apply a hybrid job-only filter", default=False)

class JobInfo(BaseModel):
    company: str = Field(description="The company's name")
    company_url: str = Field(description="LinkedIn Company URL")
    description: str = Field(description="The job description")
    is_verified: bool = Field(description="Whether the company has been verified")
    job_title: str = Field(description="Job Title")
    job_url: str = Field(description="LinkedIn Job URL")
    location: str = Field(description="Location")
    work_type: Optional[str] = Field(description="OnSite/Remote/Hybrid status", default="Remote")
    posted_at: str = Field(description="Posting date")
    score: Optional[float] = Field(description="Assigned score by LLM", default=0)
    explanation: Optional[str] = Field(description="Short explanation as to why the score was given", default="None") 

