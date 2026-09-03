from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[1]

# Force forward slashes for Windows compatibility with SQLAlchemy
DB_PATH = (BASE_DIR / "sample_project.db").as_posix()

class Settings(BaseSettings):
    database_url: str = Field(default=f"sqlite:///{DB_PATH}")

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()

# # --- ADD THIS TEMPORARY DEBUG LINE ---
# print(f"DEBUG: Database will be created at: {DB_PATH}")
# print(f"DEBUG: Final DATABASE_URL is: {settings.database_url}")
# # -------------------------------------