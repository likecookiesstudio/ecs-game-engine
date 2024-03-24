from pydantic import BaseModel


class Request(BaseModel): ...


class Auth(Request):
    username: str
