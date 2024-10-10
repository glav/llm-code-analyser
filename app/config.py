import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

ENDPOINT_URL = os.getenv("ENDPOINT_URL")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
API_VERSION = os.getenv("API_VERSION")
LOCAL_LLM_MODEL_NAME = os.getenv("LOCAL_LLM_MODEL_NAME") or "llama3.1"

all_vars = [
    "ENDPOINT_URL",
    "AZURE_OPENAI_API_KEY",
    "API_VERSION",
    "LOCAL_LLM_MODEL_NAME",
]
# Validate that the environment variables are not empty
for var in all_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} environment variable is not set or empty")


def show_config(args):
    print("-- Configuration used --")
    print(f"    ENDPOINT_URL: {ENDPOINT_URL}")
    print(f"    LOCAL_LLM_MODEL_NAME: {LOCAL_LLM_MODEL_NAME}")
    print(f"    Solution Path: [{args.solutionpath}]")
