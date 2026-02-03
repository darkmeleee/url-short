from pydantic import BaseModel, EmailStr, HttpUrl


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LinkCreate(BaseModel):
    url: HttpUrl


class LinkOut(BaseModel):
    key: str
    target_url: str
    owner_id: int | None

    class Config:
        orm_mode = True
