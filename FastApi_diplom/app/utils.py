# utils.py
from werkzeug.security import generate_password_hash,check_password_hash

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием функции generate_password_hash."""
    return generate_password_hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет, соответствует ли введённый пароль хэшированному паролю."""
    return check_password_hash(hashed_password, plain_password)