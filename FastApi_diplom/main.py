from fastapi import FastAPI, HTTPException, Depends, Request
import logging
from app.models import User, Base  # Убедитесь, что импорт правильный
from app.db import SessionLocal, engine, get_db  # Импортируйте ваши функции и классы
from app.schemas import UserCreate, UserLogin  # Импортируйте ваши схемы
from app.utils import hash_password  # Импортируйте функцию для хэширования паролей
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Произошла ошибка: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Произошла ошибка на сервере."},
    )


# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Регистрация пользователя
@app.post("/users/", response_model=UserLogin)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Попытка регистрации пользователя: {user.username}")

    # Проверка на совпадение паролей
    if user.password != user.password_repeat:
        logger.warning("Пароли не совпадают.")
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    # Проверка на существование имени пользователя
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        logger.warning(f"Имя пользователя {user.username} уже зарегистрировано.")
        raise HTTPException(status_code=400, detail="Имя пользователя уже зарегистрировано")

    # Проверка на существование email
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        logger.warning(f"Email {user.email} уже зарегистрирован.")
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    # Хэширование пароля
    hashed_password = hash_password(user.password)

    # Создание нового пользователя
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    logger.info(f"Пользователь {user.username} успешно зарегистрирован.")
    return db_user
