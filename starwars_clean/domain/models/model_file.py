from pydantic import BaseModel
from typing import List
from datetime import datetime


# Step 1: Define Pydantic model
class File(BaseModel):
    name: str
    created_date: datetime
