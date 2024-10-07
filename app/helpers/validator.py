from app.config import config
from fastapi import Header, HTTPException


async def get_token_header(authorization: str = Header(...)):
    if authorization != config.get('ADMIN_TOKEN'):
        raise HTTPException(status_code=400, detail="Authorization token is invalid")
