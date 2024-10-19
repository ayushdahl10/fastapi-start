from typing import Any
from passlib.hash import pbkdf2_sha256


def hash_password(password: str) -> Any:
    hash = pbkdf2_sha256.hash(password)
    return hash


def verify_password(password: str, salt) -> bool:
    return pbkdf2_sha256.verify(password, salt)
