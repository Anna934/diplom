from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from app.db import create_db_and_tables, get_db
from app.models import User
from app.schemas import UserCreate, UserLogin
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
# Настройка аутентификации
auth_backend = JWTAuthentication(secret="SECRET", lifetime_seconds=3600)

# Создание экземпляра FastAPI
app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание базы данных и таблиц
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Настройка маршрутов для пользователей
fastapi_users = FastAPIUsers(
    get_db,
    [auth_backend],
    User,
    UserCreate,    # Схема для создания пользователя
    UserLogin
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserLogin),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(fastapi_users.get_current_active_user)):
    return {"message": f"Hello {user.email}!"}
