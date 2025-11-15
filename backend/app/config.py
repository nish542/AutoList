from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    Application configuration settings
    """
    
    # API Configuration
    api_title: str = "Amazon Listing Generator API"
    api_version: str = "1.0.0"
    api_description: str = "Generate Amazon product listings from social media posts"
    
    # CORS settings
    cors_origins: list = ["http://localhost:5173", "http://localhost:3000"]
    
    # Model settings
    use_gpu: bool = False
    model_cache_dir: str = "./models"
    
    # Feature extraction settings
    max_image_size: int = 1024  # Max dimension for image processing
    max_text_length: int = 2000  # Max characters for text input
    
    # Listing generation settings
    default_brand: str = "Generic"
    default_material: str = "High Quality"
    min_bullets: int = 3
    max_bullets: int = 5
    
    # Export settings
    csv_encoding: str = "utf-8"
    excel_engine: str = "openpyxl"
    
    # File upload settings
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_extensions: list = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    
    # API Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60  # seconds
    
    # Logging
    log_level: str = "INFO"
    log_file: Optional[str] = "app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()


