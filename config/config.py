from pydantic_settings import BaseSettings
from typing import Optional

class OpenSkyConfig(BaseSettings):
    """Configuration for OpenSky Network API"""
    min_latitude: float = -35.0
    max_latitude: float = 15.0
    min_longitude: float = -85.0
    max_longitude: float = -30.0
    pages: int = 40
    delay: float = 1.5

class DataConfig(BaseSettings):
    """Configuration for data processing"""
    data_dir: str = "data"
    output_file: str = "flights_sample.csv"

class Config(BaseSettings):
    """Main configuration class"""
    opensky: OpenSkyConfig = OpenSkyConfig()
    data: DataConfig = DataConfig()
    
    class Config:
        env_prefix = "NEUROEVO_" 