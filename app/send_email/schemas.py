from pydantic import BaseModel

class FormData(BaseModel):
    firstName: str
    lastName: str
    phone: str
    email: str
    telegram: str
    info: str
