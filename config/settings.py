import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

ENVIRONMENTS = {
    "demo": "https://automationintesting.online",
    "local": "http://localhost:3003",
}


@dataclass(frozen=True)
class User:
    username: str
    password: str


def admin_credentials():
    username = os.getenv("RBP_ADMIN_USER")
    password = os.getenv("RBP_ADMIN_PASSWORD")
    missing_names = []
    if username is None or username.strip() == "":
        missing_names.append("RBP_ADMIN_USER")
    if password is None or password.strip() == "":
        missing_names.append("RBP_ADMIN_PASSWORD")
    if missing_names:
        raise ValueError(
            f"Missing {missing_names} Copy .env.example to .env and fill it in."
        )
    return User(username, password)
