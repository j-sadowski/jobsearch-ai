# jobsearch-ai

`jobsearch-ai` is a command-line tool that uses large language models (LLMs) to automate and enhance the job search process. It fetches job postings from LinkedIn, scores them against your resume using AI, and helps you identify the best matches.  
Inspired by an agentic job search [repo](https://github.com/Husseinjd/job-search-2.0).  

If you are interested in using the Ollama backend, make sure you have Ollama installed and the proper model specified.



## Application Workflow

![Diagram of how the application calls various components](./workflow.png)

## Features

- LLM extracts the job title and other parameters needed for fetch
- Fetches job postings from LinkedIn based on job title and city.
- Uses LLMs to evaluate and score how well your resume matches each job posting.
- Provides explanations for each score to help you understand your fit.
- Summarizes missing skills or experiences to help you improve your resume.
- Supports filtering for hybrid/remote jobs.
- Outputs the top job matches for your review.
- Saves all results and improvement suggestions to a cache file.

## Requirements

- Only tested on Python 3.13.5
- OpenAI API key
- Apify API key


## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/j-sadowski/jobsearch-ai.git
    cd jobsearch-ai
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set your up `.env` file:
    ```
    AI_BACKEND=either "openai" or "ollama"
    OPENAI_API_KEY=your_openai_api_key_here
    APIFY_API_KEY=your_apify_api_key_here
    ```

## Usage

Prepare your resume as a plain text file (e.g., `resume.txt`).

Run the tool from the command line:

```sh
python main.py -r resume.txt -p "Search for Data Scientist jobs in Austin, limit 10"
```

### Arguments

- `-r, --resume_path` (required): Path to your resume in `.txt` format.
- `-p, --prompt` (required): A prompt detailing keywords, city, optional hybrid status, and optional limit.

## Project Structure

```
jobsearch-ai/
├── main.py                # Entry point for the CLI tool
├── config.py              # Loads environment variables and configures logging
├── eval_cache.py          # Tool for testing reproducibility logic
├── job_boards/
│   └── linkedin.py        # LinkedIn job fetching logic
├── scoring/
│   ├── job_posts.py       # Job scoring logic
|   ├── ollama_models.py   # Ollama code
│   └── oa_models.py       # LLM interaction and scoring models
├── datamodels/
│   └── models.py          # Data models for job postings
├── data/
│   └── cache/             # Cached results (JSON files)
├── requirements.txt
└── README.md
```