from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://jobinsight_user:jobinsight_password@db:5432/jobinsight_db"
    QDRANT_URL: str = "http://qdrant:6333"
    REDIS_URL: str = "redis://redis:6379/0"
    JWT_SECRET: str = "supersecretkeychangeinproduction"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # --- Scraping ---
    SCRAPING_DEFAULT_PAGES: int = 3  # Nombre de pages LinkedIn à scraper par défaut
    SCRAPE_DEFAULT_KEYWORDS: str = "Data Scientist"  # Mots-clés par défaut
    SCRAPE_DEFAULT_LOCATION: str = "France"  # Localisation par défaut

    class Config:
        env_file = ".env"

settings = Settings()
