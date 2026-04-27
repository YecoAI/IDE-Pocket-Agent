import os
import base64
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    logger.critical("JWT_SECRET_KEY not set! Backend cannot start without a secure secret key.")
    raise RuntimeError("JWT_SECRET_KEY environment variable is missing. Check .env file.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

OTP_ENCRYPTION_KEY = os.getenv("OTP_ENCRYPTION_KEY")
if not OTP_ENCRYPTION_KEY:
    logger.critical("OTP_ENCRYPTION_KEY not set! Backend cannot start without an encryption key.")
    raise RuntimeError("OTP_ENCRYPTION_KEY environment variable is missing. Check .env file.")

try:
    _fernet = Fernet(OTP_ENCRYPTION_KEY)
except Exception as e:
    logger.error(f"Invalid OTP_ENCRYPTION_KEY: {e}.")
    raise RuntimeError("OTP_ENCRYPTION_KEY is invalid. It must be a 32-byte base64 encoded string.")


def encrypt_secret(plain_text: str) -> Optional[str]:
    if not plain_text:
        return None
    return _fernet.encrypt(plain_text.encode()).decode()


def decrypt_secret(cipher_text: str) -> Optional[str]:
    if not cipher_text:
        return None
    try:
        return _fernet.decrypt(cipher_text.encode()).decode()
    except Exception as e:
        logger.error(f"Decryption failed: {e}")
        return None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    sub: Optional[str] = None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        role: str = payload.get("role")
        if sub is None:
            return None
        return TokenData(username=sub, role=role, sub=sub)
    except JWTError:
        return None
