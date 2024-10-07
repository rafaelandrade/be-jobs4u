
from fastapi import APIRouter, Depends, Request
from starlette_context import context
from typing import List
from app.logger.log import logger
from app.controllers.find_jobs_controller import find_jobs_controller
from app.schemas.job_search_schema import JobSearchRequest

from app.helpers.validator import get_token_header

router = APIRouter(
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
    prefix='/jobs'
)

@router.post('/find')
async def find_jobs(request: JobSearchRequest):
    # logger.send_log('[FIND JOB] Initiation of FIND JOBS Router...', request.keywords)

    return find_jobs_controller(keywords=request.keywords, location=request.location)
