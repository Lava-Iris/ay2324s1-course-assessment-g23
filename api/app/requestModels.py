from typing import Optional
from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    password: str
    email: str

class GetUser(BaseModel):
    user_id: str