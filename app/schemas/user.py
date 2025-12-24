from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class UserMeResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)