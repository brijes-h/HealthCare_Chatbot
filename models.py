from pydantic import BaseModel

class HumanMessage(BaseModel):
    condition: str
    query: str

class ForIntent(BaseModel):
    query: str