from pyrogram import Client


def RegisterMessageHandlers(app : Client):
    @app.on_message()
    async def handle_message(client, message):
        if not message.from_user:
            return

        me = await app.get_me()
        if message.from_user.id != me.id:
            return

        if not message.text:
            return

        if message.text.lower().startswith("/run"):
            expr = message.text.split("/run", 1)[1].strip()
            try:
                result = eval(expr)
                await message.edit(
                    f"**{expr}:**\n```text\n{result}\n```",
                    parse_mode="markdown"
                )
            except Exception as e:
                await message.reply_text(f"Error: {e}")
    