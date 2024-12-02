from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import User, Base
from database import SessionLocal, engine
from schemas import UserCreate, UserResponse
from utils import hash_password

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Зависимость для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Регистрация пользователя
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
