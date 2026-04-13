from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Finance Advisor"
    debug: bool =True
    database_url: str
    secret_key: str 
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

settings=Settings()