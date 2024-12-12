# utils.py
from werkzeug.security import generate_password_hash

def hash_password(password: str) -> str:
    """Хеширует пароль с использованием функции generate_password_hash."""
    return generate_password_hash(password)
