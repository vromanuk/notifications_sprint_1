from pydantic import BaseModel


class UserRegisteredEventSchema(BaseModel):
    username: str
    email: str
