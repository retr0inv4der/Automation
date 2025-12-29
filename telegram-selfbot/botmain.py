from bot.client import Bot_Client
from bot.monitor import monitor_bot
from bot.msghandler import RegisterMessageHandlers
import asyncio

bot = Bot_Client("points.json" ,"theothersideoftheboard" )


async def main():
    app = bot.create_client()
    await app.start()
    with asyncio.TaskGroup() as tg:
        tg.create_task(RegisterMessageHandlers(app))
        tg.create_task(
            monitor_bot(
                app=app,
                bot_client=bot,
                username=bot.target_username,
            )
        )
        
if __name__ == "__main__":
    asyncio.run(main())