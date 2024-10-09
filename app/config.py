from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(".env")

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("API_VERSION")

all_vars = ["ENDPOINT_URL", "AZURE_OPENAI_API_KEY", "API_VERSION"]
# Validate that the environment variables are not empty
for var in all_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} environment variable is not set or empty")
