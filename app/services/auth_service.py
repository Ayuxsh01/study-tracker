"""
Password hashing and login/signup logic. Keeps bcrypt usage in one place
so the rest of the app never touches raw or hashed passwords directly.
"""

import bcrypt

from app.services.log_service import create_user, get_user_by_email


def hash_password(plain_password: str) -> str:
    # bcrypt works on bytes and returns bytes; we store it as a string.
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


def signup(name: str, email: str, password: str) -> dict:
    """Creates a new user. Raises ValueError if the email is already taken."""
    if get_user_by_email(email) is not None:
        raise ValueError("An account with this email already exists.")

    password_hash = hash_password(password)
    user_id = create_user(name=name, email=email, password_hash=password_hash)
    return {"id": user_id, "name": name, "email": email}


def login(email: str, password: str) -> dict | None:
    """Returns the user dict if credentials are correct, otherwise None."""
    user = get_user_by_email(email)
    if user is None:
        return None
    if not verify_password(password, user["password_hash"]):
        return None
    return {"id": user["id"], "name": user["name"], "email": user["email"]}
