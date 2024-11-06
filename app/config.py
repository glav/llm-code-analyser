import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
LOCAL_LLM_MODEL_NAME = os.getenv("LOCAL_LLM_MODEL_NAME") or "llama3.1"
AZURE_LLM_MODEL_NAME = os.getenv("AZURE_LLM_MODEL_NAME") or "gpt-4o"
LLM_MODE = os.getenv("LLM_MODE") or "local"

all_vars = [
    # "AZURE_OPENAI_ENDPOINT",
    # "AZURE_OPENAI_API_KEY",
    # "AZURE_API_VERSION",
    "LOCAL_LLM_MODEL_NAME",
]
# Validate that the environment variables are not empty
for var in all_vars:
    if not os.getenv(var):
        raise ValueError(f"{var} environment variable is not set or empty")


def show_config(args):
    print("-- Configuration used --")
    print(f"    LLM_MODE: {LLM_MODE}")
    if LLM_MODE == "azure":
        print(f"    AZURE_API_VERSION: {AZURE_API_VERSION}")
        print(f"    AZURE_ENDPOINT_URL: {AZURE_OPENAI_ENDPOINT}")
        print(f"    AZURE_LLM_MODEL_NAME: {AZURE_LLM_MODEL_NAME}")
    else:
        print(f"    LOCAL_LLM_MODEL_NAME: {LOCAL_LLM_MODEL_NAME}")
    print(f"    Solution Path: [{args.solutionpath}]")
