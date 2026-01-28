from pydantic import BaseModel

class CareerQuery(BaseModel):
    query: str
    top_k: int = 5


class CareerResponse(BaseModel):
    answer: str
