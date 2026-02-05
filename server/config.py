import os
import redis
from dotenv import load_dotenv

load_dotenv()

class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SESSION_TYPE = "redis"
    
    SESSION_PERMANENT = False
    
    SESSION_USE_SIGNER = True
    
    PERMANENT_SESSION_LIFETIME = 1800 

    SESSION_REDIS = redis.from_url(os.environ.get("REDIS_URL", "redis://127.0.0.1:6379"))

    DB_PATH = os.path.join(os.path.dirname(__file__), "data", "portfolio.db")