from typing import List
from fastapi import HTTPException
from app.services.find_jobs_services import find_jobs_services


def find_jobs_controller(keywords: List[str], location: str):
    print("CONTROLLER -> ", keywords, location)
    try:
        return find_jobs_services(keywords=keywords, location=location)
    except HTTPException:
        raise HTTPException(status_code=500, detail={"error": True})