import os
import json
import logging
import win32crypt
from typing import Optional, Dict, Any
from src.config import settings

logger = logging.getLogger(__name__)

def load_credentials() -> Optional[Dict[str, Any]]:
    creds_path = settings.credentials_path
    if not os.path.exists(creds_path):
        return None
        
    try:
        with open(creds_path, "rb") as f:
            encrypted_data = f.read()
        
        _, decrypted_data = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)
        creds = json.loads(decrypted_data.decode("utf-8"))
        
        if not all(k in creds for k in ("access_token", "association_id")):
            return None
            
        return creds
    except Exception:
        return None

def save_credentials(token: str, association_id: str) -> bool:
    if not token or not association_id:
        return False
        
    try:
        data = json.dumps({
            "access_token": token,
            "association_id": str(association_id)
        }).encode("utf-8")
        
        encrypted_data = win32crypt.CryptProtectData(data, "TRAE-Mobile-Agent Credentials", None, None, None, 0)
        
        with open(settings.credentials_path, "wb") as f:
            f.write(encrypted_data)
            
        return True
    except Exception:
        return False

def clear_credentials() -> bool:
    try:
        creds_path = settings.credentials_path
        if os.path.exists(creds_path):
            os.remove(creds_path)
            return True
        return False
    except Exception:
        return False
