import asyncio
from pyrogram import Client 
from pyrogram.enums import ParseMode

import os
import dotenv
from math import *
from datetime import date , datetime

dotenv.load_dotenv()
api_id = os.getenv("TEL_API_ID")
api_hash = os.getenv("TEL_API_HASH")
proxy = {
    "scheme": "MTPROTO",  # "socks4", "socks5" and "http" are supported
    "hostname": "65.109.147.218",
    "port": 433,
    "credentials" : "EERighJJvXrFGRMCIMJdCQ"
}
app = Client("my_account" )

@app.on_message()
async def handle_message(client, message ):
    # check if the "calc" string is in the message text and then calculate the expression after it and reply a message to the message sender
    #handle the uppercase and lowercase of "calc"
    #check if the sender is me
    if message.from_user.id == (await app.get_me()).id:
        
        if "/run" in message.text.lower():
            message.text = message.text.lower()
            expression = message.text.split("/run",1)[1].strip()
            try:
                result = eval(expression)
                #edit my message instead of sending a new one
                #put the messge in markdown format
                await message.edit(f"**{expression}:**\n ```text\n{result}\n``` " , parse_mode=ParseMode.MARKDOWN)
                
                
            except Exception as e:
                await message.reply_text(f"Error in calculation: {e}")
                pass
        print(f"Received message: {message.text}")
    

    
app.run()
