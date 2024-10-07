import requests
from typing import List, Optional
from fastapi import HTTPException
from app.logger.log import logger

from app.config import config

# Base URL for Adzuna API
ADZUNA_BASE_URL = "http://api.adzuna.com/v1/api/jobs/{location}/search/1"

# Adzuna API credentials
ADZUNA_APP_ID = config['ADZUNA_ID']  # Replace with your actual App ID
ADZUNA_APP_KEY = config['ADZUNA_API_KEY']  # Replace with your actual App Key


def build_adzuna_search_url(keywords: List[str], location: str):
    keywords_str = "%20".join(keywords)  # Join keywords with spaces

    # Format the URL with the specified location (e.g., 'gb' for Great Britain)
    location = location.lower()

    URL_WITH_PARAMS = f"http://api.adzuna.com/v1/api/jobs/gb/search/1?app_id={ADZUNA_APP_ID}&app_key={ADZUNA_APP_KEY}&results_per_page=20&what={keywords_str}&where={location}&content-type=application/json"

    return URL_WITH_PARAMS


def search_jobs_on_adzuna(keywords: List[str], location: str = "gb"):
    url = build_adzuna_search_url(keywords=keywords, location=location)

    response = requests.get(url=url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to retrieve jobs from Adzuna")

    jobs_data = response.json()

    if "results" not in jobs_data:
        raise HTTPException(status_code=500, detail="No job results found")

    # Extracting job information from the response
    jobs = []
    for job in jobs_data['results']:
        job_info = {
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name"),
            "description": job.get("description"),
            "url": job.get("redirect_url")
        }
        jobs.append(job_info)

    return jobs


def find_jobs_services(keywords: List[str], location: str = "gb") -> any:
    try:
        return search_jobs_on_adzuna(keywords=keywords, location=location)
    except HTTPException:
        raise HTTPException(status_code=500, detail="Failed to retrieve jobs from Adzuna")
