import os
import json

from dotenv import load_dotenv
load_dotenv()

CREDENTIALS = os.getenv("CREDENTIALS", default=None)
if CREDENTIALS is None:
    raise EnvironmentError("Could not found CREDENTIALS environment variable. Please set it")

def load_credentials():
    with open(f"{CREDENTIALS}", "r") as f:
        data: dict = json.load(f)

    GOOGLE_API_PRIVATE_KEY = data.get("private_key")
    if GOOGLE_API_PRIVATE_KEY is None:
        raise OSError(f"Could not find private_key field in {CREDENTIALS}")
    
    GOOGLE_API_CLIENT_EMAIL = data.get("client_email")
    if GOOGLE_API_CLIENT_EMAIL is None:
        raise OSError(f"Could not find client_email field in {CREDENTIALS}")


    os.environ["GOOGLE_API_PRIVATE_KEY"] = GOOGLE_API_PRIVATE_KEY
    os.environ["GOOGLE_API_CLIENT_EMAIL"] = GOOGLE_API_CLIENT_EMAIL
