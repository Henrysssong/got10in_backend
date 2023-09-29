from pydantic import BaseModel, EmailStr

class Subscription(BaseModel):
    email: EmailStr