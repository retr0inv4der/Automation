from bot.config import Config, load_config
from pyrogram import Client


def create_client(client :Config):
    client = load_config()
    return Client(
        "my_account",
        api_id=client.api_id,
        api_hash=client.api_hash
    )

