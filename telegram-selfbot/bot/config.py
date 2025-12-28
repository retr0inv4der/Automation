from logging import config
import dotenv 
import os

class Config : 
    api_id : str 
    api_hash : str
    target_username : str
    alert_chat : str
    
    
def load_config() -> Config :
    dotenv.load_dotenv()
    try:
        config = Config()
        config.api_id = int(os.getenv("TEL_API_ID"))
        config.api_hash = os.getenv("TEL_API_HASH")
        if not config.api_id or not config.api_hash:
            raise RuntimeError("Missing TEL_API_ID or TEL_API_HASH")
        config.target_username = os.getenv("TARGET_USERNAME").lstrip("@")
        config.alert_chat = os.getenv("ALERT_CHAT")
        if not config.target_username:
            raise RuntimeError("Missing TARGET_USERNAME")
        if not config.alert_chat:
            raise RuntimeError("Missing ALERT_CHAT")
        return config
    
    except Exception as e:
        raise RuntimeError(f"Failed to load config: {e}")