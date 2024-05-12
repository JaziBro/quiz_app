from starlette.config import Config
from datetime import timedelta

try:
    config = Config(".env")
except FileNotFoundError as e:
    config = Config()

db = config.get("DATABASE_URL")
testDB = config.get("TEST_DATABASE_URL")
AccessTokenExpiryTime = timedelta(minutes=int(config.get("ACCESS_EXPIRY_TIME")))
RefreshTokenExpiryTime = timedelta(days=int(config.get("REFRESH_EXPIRY_TIME")))
secretKey = config.get("SECRET_KEY")
algorithm= config.get("ALGORITHM")


