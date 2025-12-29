from bot.client import Bot_Client
from pyrogram import Client
import time
async def monitor_bot(
    app: Client,
    bot_client: Bot_Client,
    username: str,
    
):
    await app.send_message(bot_client.alert_chat, f"Started monitoring bot for @{username}.")
    
    