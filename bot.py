import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from datetime import datetime, timedelta
import json
import os
import re

API_ID = "10115546"
API_HASH = "366347107f54aabc951cfa9d3c2fb2ce"
BOT_TOKEN = "7483230333:AAEMe6N4lvwad-As6EW9soCr7PsggI-Zzs4"

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load users, groups, and channels from a JSON file
def load_data():
    if not os.path.exists("data.json"):
        return {"users": [], "groups": [], "channels": []}
    with open("data.json", "r") as f:
        return json.load(f)

# Save users, groups, and channels to a JSON file
def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

data = load_data()

async def schedule_message(client, chat_id, text, interval):
    while True:
        await client.send_message(chat_id, text)
        await asyncio.sleep(interval)

@app.on_message(filters.command("broadcast") & filters.user(data["users"]))
async def broadcast(client, message: Message):
    text = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
    for user_id in data["users"]:
        await client.send_message(user_id, text)
    await message.reply("Broadcast message sent to all users.")

@app.on_message(filters.command("broadcastgroup") & filters.user(data["users"]))
async def broadcast_group(client, message: Message):
    text = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
    for group_id in data["groups"]:
        await client.send_message(group_id, text)
    await message.reply("Broadcast message sent to all groups.")

@app.on_message(filters.command("broadcastchannel") & filters.user(data["users"]))
async def broadcast_channel(client, message: Message):
    text = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
    for channel_id in data["channels"]:
        await client.send_message(channel_id, text)
    await message.reply("Broadcast message sent to all channels.")

@app.on_message(filters.command("broadcastall") & filters.user(data["users"]))
async def broadcast_all(client, message: Message):
    text = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else ""
    for user_id in data["users"]:
        await client.send_message(user_id, text)
    for group_id in data["groups"]:
        await client.send_message(group_id, text)
    for channel_id in data["channels"]:
        await client.send_message(channel_id, text)
    await message.reply("Broadcast message sent to all users, groups, and channels.")

@app.on_message(filters.command("scheduleuser") & filters.user(data["users"]))
async def schedule_user(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a time interval (e.g., now:8hour).")
        return

    interval = message.command[1]
    match = re.match(r'now:(\d+)(\w+)', interval)
    if not match:
        await message.reply("Invalid format. Use now:<number><unit> (e.g., now:8hour).")
        return

    number, unit = int(match.group(1)), match.group(2)
    seconds = number * 3600 if unit == "hour" else number * 60 if unit == "minute" else 0

    if seconds == 0:
        await message.reply("Invalid time unit. Use 'hour' or 'minute'.")
        return

    text = message.reply_to_message.text if message.reply_to_message else "Scheduled message"
    for user_id in data["users"]:
        asyncio.create_task(schedule_message(client, user_id, text, seconds))

@app.on_message(filters.command("schedulegroup") & filters.user(data["users"]))
async def schedule_group(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a time interval (e.g., now:8hour).")
        return

    interval = message.command[1]
    match = re.match(r'now:(\d+)(\w+)', interval)
    if not match:
        await message.reply("Invalid format. Use now:<number><unit> (e.g., now:8hour).")
        return

    number, unit = int(match.group(1)), match.group(2)
    seconds = number * 3600 if unit == "hour" else number * 60 if unit == "minute" else 0

    if seconds == 0:
        await message.reply("Invalid time unit. Use 'hour' or 'minute'.")
        return

    text = message.reply_to_message.text if message.reply_to_message else "Scheduled message"
    for group_id in data["groups"]:
        asyncio.create_task(schedule_message(client, group_id, text, seconds))

    await message.reply("Scheduled message to all groups.")

@app.on_message(filters.command("schedulechannel") & filters.user(data["users"]))
async def schedule_channel(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a time interval (e.g., now:8hour).")
        return

    interval = message.command[1]
    match = re.match(r'now:(\d+)(\w+)', interval)
    if not match:
        await message.reply("Invalid format. Use now:<number><unit> (e.g., now:8hour).")
        return

    number, unit = int(match.group(1)), match.group(2)
    seconds = number * 3600 if unit == "hour" else number * 60 if unit == "minute" else 0

    if seconds == 0:
        await message.reply("Invalid time unit. Use 'hour' or 'minute'.")
        return

    text = message.reply_to_message.text if message.reply_to_message else "Scheduled message"
    for channel_id in data["channels"]:
        asyncio.create_task(schedule_message(client, channel_id, text, seconds))

    await message.reply("Scheduled message to all channels.")

@app.on_message(filters.command("scheduleall") & filters.user(data["users"]))
async def schedule_all(client, message: Message):
    if len(message.command) < 2:
        await message.reply("Please provide a time interval (e.g., now:8hour).")
        return

    interval = message.command[1]
    match = re.match(r'now:(\d+)(\w+)', interval)
    if not match:
        await message.reply("Invalid format. Use now:<number><unit> (e.g., now:8hour).")
        return

    number, unit = int(match.group(1)), match.group(2)
    seconds = number * 3600 if unit == "hour" else number * 60 if unit == "minute" else 0

    if seconds == 0:
        await message.reply("Invalid time unit. Use 'hour' or 'minute'.")
        return

    text = message.reply_to_message.text if message.reply_to_message else "Scheduled message"
    for user_id in data["users"]:
        asyncio.create_task(schedule_message(client, user_id, text, seconds))
    for group_id in data["groups"]:
        asyncio.create_task(schedule_message(client, group_id, text, seconds))
    for channel_id in data["channels"]:
        asyncio.create_task(schedule_message(client, channel_id, text, seconds))

    await message.reply("Scheduled message to all users, groups, and channels.")

@app.on_message(filters.command("total") & filters.user(data["users"]))
async def total(client, message: Message):
    total_users = len(data["users"])
    total_groups = len(data["groups"])
    total_channels = len(data["channels"])
    await message.reply(f"Total Users: {total_users}, Total Groups: {total_groups}, Total Channels: {total_channels}")

@app.on_message(filters.command("adduser") & filters.user(data["users"]))
async def add_user(client, message: Message):
    user_id = int(message.text.split(" ")[1])
    if user_id not in data["users"]:
        data["users"].append(user_id)
        save_data(data)
        await message.reply(f"User {user_id} added.")
    else:
        await message.reply("User already exists.")

 @app.on_message(filters.command("deluser") & filters.user(data["users"]))

 async def delete_user(client, message: Message):
     user_id = int(message.text.split(" ")[1])
     if user_id in data["users"]:
         data["users"].remove(user_id)
         save_data(data)
         await message.reply(f"User {user_id} deleted.")
     otherwise:
         await message.reply("User not found.")
   
if __name__ == "__main__":
    app.run()
