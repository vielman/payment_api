import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    USERNAME:str = os.getenv('USERNAME')
    PASSWORD:str = os.getenv('PASSWORD')
    GRANT_TYPE:str = os.getenv('GRANT_TYPE')
    CLIENT_ID:str = os.getenv('CLIENT_ID')
    CLIENT_SECRET:str = os.getenv('CLIENT_SECRET')
    PAYPERTIC_URL_AUTH:str = os.getenv('PAYPERTIC_URL_AUTH')
    PAYPERTIC_URL_HOST:str = os.getenv('PAYPERTIC_URL_HOST')
    HOST_API:str = os.getenv('HOST_API')
    PAYLOAD:str = f"username={USERNAME}&password={PASSWORD}&grant_type={GRANT_TYPE}&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}"

    ISPCUBE_URL_HOST:str = os.getenv('ISPCUBE_URL_HOST')
    USERNAME_ISPCUBE:str = os.getenv('USERNAME_ISPCUBE')
    PASSWORD_ISPCUBE:str = os.getenv('PASSWORD_ISPCUBE')
    CLIENT_ID_ISPCUBE:str = os.getenv('CLIENT_ID_ISPCUBE')
    API_KEY:str = os.getenv('API_KEY')
    LOGIN_TYPE:str = os.getenv('LOGIN_TYPE')

settings = Settings()