import os
import json
import logging
import sys
from typing import Optional, Dict, Any
from src.config import settings

if sys.platform == "win32":
    try:
        import win32crypt
    except ImportError:
        win32crypt = None
else:
    try:
        import keyring
    except ImportError:
        keyring = None

logger = logging.getLogger(__name__)

KEYRING_SERVICE = "IDE-Pocket-Agent"
KEYRING_ACCOUNT = "agent_credentials"

def load_credentials() -> Optional[Dict[str, Any]]:
    if sys.platform != "win32" and keyring:
        try:
            data = keyring.get_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
            if data:
                creds = json.loads(data)
                if all(k in creds for k in ("access_token", "association_id")):
                    return creds
        except Exception as e:
            logger.debug(f"Keyring load failed: {e}")

    # 2. Try DPAPI (Windows fallback/primary)
    creds_path = settings.credentials_path
    if not os.path.exists(creds_path):
        return None
        
    try:
        with open(creds_path, "rb") as f:
            encrypted_data = f.read()
        
        if sys.platform == "win32" and win32crypt:
            _, decrypted_data = win32crypt.CryptUnprotectData(encrypted_data, None, None, None, 0)
            creds = json.loads(decrypted_data.decode("utf-8"))
            if all(k in creds for k in ("access_token", "association_id")):
                return creds
        else:
            creds = json.loads(encrypted_data.decode("utf-8"))
            return creds
    except Exception:
        return None
    return None

def save_credentials(token: str, association_id: str) -> bool:
    if not token or not association_id:
        return False
        
    creds_dict = {
        "access_token": token,
        "association_id": str(association_id)
    }
    data_str = json.dumps(creds_dict)

    # 1. Use Keyring on macOS/Linux
    if sys.platform != "win32" and keyring:
        try:
            keyring.set_password(KEYRING_SERVICE, KEYRING_ACCOUNT, data_str)
            return True
        except Exception as e:
            logger.error(f"Keyring save failed: {e}")

    # 2. Use DPAPI on Windows
    try:
        data_bytes = data_str.encode("utf-8")
        if sys.platform == "win32" and win32crypt:
            encrypted_data = win32crypt.CryptProtectData(data_bytes, "IDE-Pocket-Agent Credentials", None, None, None, 0)
        else:
            encrypted_data = data_bytes # No encryption fallback
            
        with open(settings.credentials_path, "wb") as f:
            f.write(encrypted_data)
            
        return True
    except Exception:
        return False

def clear_credentials() -> bool:
    success = False
    # Clear Keyring
    if sys.platform != "win32" and keyring:
        try:
            keyring.delete_password(KEYRING_SERVICE, KEYRING_ACCOUNT)
            success = True
        except Exception:
            pass

    # Clear File
    try:
        creds_path = settings.credentials_path
        if os.path.exists(creds_path):
            os.remove(creds_path)
            success = True
    except Exception:
        pass
    return success
