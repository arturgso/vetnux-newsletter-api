from pydantic import BaseModel, EmailStr

class SubscriberCreate(BaseModel):
    email: EmailStr
    
class SubscriberOut(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True