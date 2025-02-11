from pydantic import BaseModel, Field

class EmailDeleteRequest(BaseModel):
    days_old: int = Field(..., gt=0, description="Number of days old emails to delete (must be greater than 0)")