import asyncio
import time
import os
import json
from pathlib import Path
import dotenv

from pyrogram import Client, idle
from pyrogram.enums import ParseMode


dotenv.load_dotenv()

api_id = int(os.getenv("TEL_API_ID")) if os.getenv("TEL_API_ID") else None
api_hash = os.getenv("TEL_API_HASH")

if not api_id or not api_hash:
    raise RuntimeError("Missing TEL_API_ID or TEL_API_HASH")

target_username = os.getenv("TARGET_USERNAME").lstrip("@")
alert_chat = os.getenv("ALERT_CHAT")


app = Client(
    "my_account",
    api_id=api_id,
    api_hash=api_hash
)


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
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await message.reply_text(f"Error: {e}")


POINTS_FILE = Path("points.json")

def load_points():
    if not POINTS_FILE.exists():
        return {}
    try:
        return json.loads(POINTS_FILE.read_text())
    except Exception:
        return {}

def save_points(data: dict):
    try:
        POINTS_FILE.write_text(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[!] Failed saving points: {e}")

async def monitor_user(
    username: str,
    check_interval: float = 5.0,
    award_interval: float = 30 * 60.0,  #30 mins
    online_threshold: float = 10.0,
):
    points = load_points()
    user_key = username.lower()
    if user_key not in points:
        points[user_key] = {"total": 0}

    offline_start = None
    awarded_chunks = 0

    online_start = None
    last_alert_time = None

    await app.send_message(alert_chat, f"Started monitoring @{username}.")

    while True:
        try:
            user = await app.get_users(username)

            is_online = False
            if hasattr(user, "is_online"):
                is_online = user.is_online
            elif hasattr(user, "status") and user.status:
                is_online = "online" in str(user.status).lower()

            now = time.time()

            if is_online:
                if online_start is None:
                    online_start = now
                    last_alert_time = now
                    print(f"[+] {username} came online")

                if (now - last_alert_time) >= online_threshold:
                    elapsed = int(now - online_start)
                    text = (
                        f"🚨 ONLINE ALERT 🚨\n"
                        f"@{username} has been online for {elapsed} seconds."
                    )
                    try:
                        await app.send_message(alert_chat, text)
                    except Exception:
                        try:
                            await app.send_message("me", text)
                        except Exception:
                            print("[!] Failed to send online alert")
                    last_alert_time = now


                if offline_start is not None:
                    print(f"[-] {username} came online — resetting focus timer")
                offline_start = None
                awarded_chunks = 0

            else:
                if offline_start is None:
                    offline_start = now
                    awarded_chunks = 0
                    print(f"[+] {username} went offline — starting focus timer")

                offline_elapsed = now - offline_start
                chunks = int(offline_elapsed // award_interval)

                if chunks > awarded_chunks:
                    new_chunks = chunks - awarded_chunks
                    awarded_chunks = chunks


                    points[user_key]["total"] += new_chunks
                    save_points(points)


                    msg = (
                        f"🎯 Focus reward: +{new_chunks} point(s)\n"
                        f"Total points: {points[user_key]['total']}"
                    )
                    try:
                        await app.send_message(user.id, msg)
                    except Exception:
                        await app.send_message(alert_chat, f"Could not DM @{username}. {msg}")


                if online_start is not None:
                    online_start = None
                    last_alert_time = None

        except Exception as e:
            print(f"[!] Monitor error: {e}")

        await asyncio.sleep(check_interval)


async def main():
    await app.start()
    asyncio.create_task(
        monitor_user(
            username=target_username,
            check_interval=2.0,
            online_threshold=10.0
        )
    )
    print(f"Monitoring @{target_username}")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
