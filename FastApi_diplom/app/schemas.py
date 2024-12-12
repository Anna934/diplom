from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Поле для электронной почты
    password: str
    repeat_password: str

@field_validator('repeat_password')
def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
class User(UserCreate):
    id: int
class UserLogin(BaseModel):
    username: str
    password: str