from pydantic import BaseModel

class EmailDeleteRequest(BaseModel):
    days_old: int
