from pydantic import BaseModel
from typing import List

class JobSearchRequest(BaseModel):
    keywords: List[str]
    location: str