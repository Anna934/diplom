
from typing import Optional
from sqlalchemy.orm import Session
from app.models import User  # Импортируйте ваш класс User
from werkzeug.security import generate_password_hash, check_password_hash  # Для хеширования паролей

class SimpleUserManager:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, username: str, email: str, password: str) -> User:
        hashed_password = generate_password_hash(password)  # Хешируем пароль
        user = User(
            username=username,
            email=email,
            password=hashed_password  # Сохраняем хешированный пароль
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def verify_user(self, user: User) -> None:
        # Логика верификации пользователя
        print(f"User {user.id} has been verified.")

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.db.query(User).filter(User.email == email).first()  # Получаем пользователя по email
        if user and check_password_hash(user.password, password):  # Проверяем пароль
            return user  # Успешная аутентификация
        return None  # Неверный email или пароль

