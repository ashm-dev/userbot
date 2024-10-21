import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Settings:
    API_ID: int
    API_HASH: str
    APP_NAME: str
    
    @classmethod
    def from_env(cls, env_path: str = ".env") -> "Settings":
        load_dotenv(dotenv_path=env_path, override=True)
        
        return cls(
            API_ID=int(os.getenv("API_ID")),
            API_HASH=os.getenv("API_HASH"),
            APP_NAME=os.getenv("APP_NAME"),
        )
