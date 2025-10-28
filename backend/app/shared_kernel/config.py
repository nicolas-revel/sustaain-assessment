import os
from typing import Optional

class Config:
    
    def __init__(self):
        self.debug = self._get_bool_env("DEBUG", False)
        self.host = self._get_env("HOST", "localhost")
        self.port = self._get_int_env("PORT", 8000)
        self.database_url = self._get_env("DATABASE_URL", "sqlite:///app.db")
        self.secret_key = self._get_env("SECRET_KEY", "dev-secret-key")
        
    def _get_env(self, key: str, default: Optional[str] = None) -> str:
        return os.getenv(key, default)
    
    def _get_int_env(self, key: str, default: int) -> int:
        value = os.getenv(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        value = os.getenv(key)
        if value is None:
            return default
        return value.lower() in ("true", "1", "yes", "on")


config = Config()
