from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    client_id: str

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    user_id: int
    created_at: datetime | None= None
    last_login:datetime | None=None
    
    class config:
        orm_mode = True
        
class Token(BaseModel):
    access_token: str
    token_type: str