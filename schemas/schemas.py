# models.py
from pydantic import BaseModel
# --- Token Models ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str | None = None
    id: str
    role: str
