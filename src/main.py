from dotenv import load_dotenv
import os

load_dotenv()  # This line brings all environment variables from .env into os.environ

BARD_API_KEY = os.environ.get("BARD_API_KEY");