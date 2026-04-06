import os
import logging
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

logger = logging.getLogger(__name__)

class Theme:
    FONT_FAMILY = "Inter"
    FONT_MONO = "JetBrains Mono"
    BG_BASE = "#0a0b0d"
    BG_SECONDARY = "#121314"
    TEXT_DEFAULT = "#f5f9fe"
    TEXT_SECONDARY = "#a6aab5"
    TEXT_MUTED = "#787d87"
    BRAND_GREEN = "#32f08c"
    BRAND_GREEN_HOVER = "#0fdc78"
    PRIMARY_BLUE = "#387bff"
    ERROR_RED = "#f64d46"
    BORDER_SUBTLE = "#2a2d31"

class Settings(BaseSettings):
    backend_url: str = "https://api-tm.yecoai.com"
    trae_license_key: str = "TRAE-MOBILE-BETA-2026"
    
    @field_validator("backend_url")
    @classmethod
    def validate_backend_url(cls, v: str) -> str:
        if v.startswith("http://"):
            logger.warning("SECURITY WARNING: Unsafe URL detected (HTTP). Forcing upgrade to HTTPS.")
            return v.replace("http://", "https://", 1)
        if not v.startswith("https://"):
            logger.error("Invalid BACKEND_URL. Must start with https://.")
            raise ValueError("Invalid URL scheme")
        return v.rstrip("/")

    @property
    def ws_url(self) -> str:
        return self.backend_url.replace("https://", "wss://")

    @property
    def credentials_path(self) -> str:
        appdata = os.getenv("APPDATA")
        if not appdata:
            return os.path.join(os.getcwd(), "agent_credentials.dat")
        
        folder = os.path.join(appdata, "TRAE-Mobile-Agent")
        try:
            os.makedirs(folder, mode=0o700, exist_ok=True)
        except Exception:
            return os.path.join(os.getcwd(), "agent_credentials.dat")
            
        return os.path.join(folder, "agent_credentials.dat")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
