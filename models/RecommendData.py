from pydantic import BaseModel
from typing import List
from typing import Optional

class RecommendData(BaseModel):
    data: List[List[int]]
    quantity: int