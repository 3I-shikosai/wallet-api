from pydantic import BaseModel


# ------------- User Wallet --------------


class UserLogin(BaseModel):
    user_id: str
    api_key: str


class UserSync(BaseModel):
    user_id: str
    api_key: str


# ---------------- Admin ------------------


class UserCreate(BaseModel):
    password: str


class UserDelete(BaseModel):
    user_id: str
    password: str


class GetBalance(BaseModel):
    user_id: str
    password: str


class SetBalance(BaseModel):
    user_id: str
    password: str
    balance: int


# -------------- Common ------------------


class UserData(BaseModel):
    user_id: str
    balance: int
