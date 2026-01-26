from pydantic import BaseModel
from typing import List

class QueryVariations(BaseModel):
    queries: List[str]