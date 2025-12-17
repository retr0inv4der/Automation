import asyncio
from pyrogram import Client
import os
import dotenv
from math import *

dotenv.load_dotenv()
api_id = os.getenv("TEL_API_ID")
api_hash = os.getenv("TEL_API_HASH")

app = Client("my_account")

@app.on_message()
async def handle_message(client, message):
    # check if the "calc" string is in the message text and then calculate the expression after it and reply a message to the message sender
    #handle the uppercase and lowercase of "calc"
    if "calc" in message.text.lower():
        message.text = message.text.lower()
        expression = message.text.split("calc",1)[1].strip()
        try:
            result = eval(expression)
            await message.reply_text(f"The result is: {result}")
        except Exception as e:
            await message.reply_text(f"Error in calculation: {e}")
            pass
    print(f"Received message: {message.text}")
    
    
    
app.run()
