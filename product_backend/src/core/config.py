from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    SQLALCHEMY_DATABASE_URI: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS
    BACKEND_CORS_ORIGINS: list[str]

    # Openai
    OPENAI_API_KEY: str

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    # Twilio
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_FROM_NUMBER: str
    TWILIO_TO_NUMBER: str

    # Mongo DB
    MONGO_URI: str

    # API Base
    API_BASE_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
