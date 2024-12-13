from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import get_db
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/signup/")
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.password != user.repeat_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")

    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Обновляем объект db_user, чтобы получить его ID и другие поля

    return {"message": f"Добро пожаловать, {user.username}!"}


@router.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    return {"message": f"С возвращением, {user.username}!"}
