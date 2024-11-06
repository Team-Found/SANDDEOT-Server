from pydantic import BaseModel
from typing import List
from typing import Optional

class RecommendData(BaseModel):
    data: List[int]
    quantity: int