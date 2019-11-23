from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

class DevelopmentConfiguration:
    CHROME_DRIVER = os.getenv("CHROME_DRIVER")

