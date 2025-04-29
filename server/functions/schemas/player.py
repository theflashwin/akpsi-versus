from pydantic import BaseModel
from typing import Dict

class Player(BaseModel):
    id: int
    first_name: str
    last_name: str
    major: str
    graduation_year: int
    pledge_class: str
    ratings: Dict[str, float]