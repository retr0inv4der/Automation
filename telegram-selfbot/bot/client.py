from bot.config import Config, load_config
from pyrogram import Client
from bot.storage import storage 



class Bot_Client(Config): 
    def __init__(self, db , user  ):
        self.config = load_config()
        self.Storage = storage(db , user )
        self.alert_chat = self.config.alert_chat
        self.target_username  = self.config.target_username
        self.app = Client(
            "my_account",
            api_id=self.config.api_id,
            api_hash= self.config.api_hash
        )
    
    def create_client(self ) -> Client :
        return self.app 
    
