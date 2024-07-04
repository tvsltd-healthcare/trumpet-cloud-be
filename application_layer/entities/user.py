from pydantic import BaseModel


class User(BaseModel):
    id: str
    firstname: str
    lastname: str
    email: str
