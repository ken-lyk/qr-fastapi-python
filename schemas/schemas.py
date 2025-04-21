# models.py
from typing import Literal
from pydantic import BaseModel, Field
# --- Token Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str | None = None
    id: str
    role: str

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    # order_by: Literal["created_at", "updated_at"] = "created_at"
    # tags: list[str] = []
