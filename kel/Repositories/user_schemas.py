from pydantic  import BaseModel


class NewUser(BaseModel):
    name :str
    surname:str
    username:str
    email: str
    password:str

class User(NewUser):

    id: str
    name: str
    surname: str
    username: str
    email: str
    password: str


class Login(BaseModel):
    username:str
    password:str



class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    key: str
