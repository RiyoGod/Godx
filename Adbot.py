import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import init
import random
from pymongo import MongoClient

init(autoreset=True)

BOT_API_ID = "26416419"
BOT_API_HASH = "c109c77f5823c847b1aeb7fbd4990cc4"
BOT_API_TOKEN = "8075027784:AAHbomx4HBS8GvZGKnOuRwcgDBMzdZTxodw"

CREDENTIALS_FOLDER = 'sessions'
MONGO_URI = "your_mongo_uri"
client = MongoClient(MONGO_URI)
db = client["autobot"]
allowed_users_collection = db["allowed_users"]

if not os.path.exists(CREDENTIALS_FOLDER):
    os.mkdir(CREDENTIALS_FOLDER)

bot = TelegramClient('bot_session', BOT_API_ID, BOT_API_HASH)

OWNER_ID = 6748827895

def get_allowed_users():
    users = set()
    for user in allowed_users_collection.find():
        users.add(user["user_id"])
    return users

ALLOWED_USERS = get_allowed_users()
ALLOWED_USERS.add(OWNER_ID)

if not allowed_users_collection.find_one({"user_id": OWNER_ID}):
    allowed_users_collection.insert_one({"user_id": OWNER_ID})

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this bot.")
        return
    await event.reply("Welcome! Use /host to host accounts, /forward to start forwarding ads, and /accounts to list accounts.")

@bot.on(events.NewMessage(pattern='/host'))
async def host_command(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return
    await event.reply("Send your API ID, API Hash, and phone number in the format:\n`API_ID|API_HASH|PHONE_NUMBER`")

@bot.on(events.NewMessage)
async def process_input(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        return

    data = event.text.split('|')
    if len(data) == 3:
        api_id, api_hash, phone_number = data
        session_name = f"{CREDENTIALS_FOLDER}/session_{user_id}_{phone_number}"
        user_client = TelegramClient(session_name, api_id, api_hash)

        try:
            await user_client.connect()
            if not await user_client.is_user_authorized():
                await user_client.send_code_request(phone_number)
                await event.reply("OTP sent to your phone. Reply with the OTP.")
            else:
                await event.reply(f"Account {phone_number} is already authorized and hosted!")
        except Exception as e:
            await event.reply(f"Error: {e}")
        return

    # OTP Handling
    if event.text.isdigit():
        otp = event.text.strip()
        for file in os.listdir(CREDENTIALS_FOLDER):
            if file.startswith(f"session_{user_id}"):
                session_name = os.path.join(CREDENTIALS_FOLDER, file)
                user_client = TelegramClient(session_name, BOT_API_ID, BOT_API_HASH)
                await user_client.connect()
                try:
                    await user_client.sign_in(phone_number, otp)
                    await event.reply("Account successfully hosted!")
                except Exception as e:
                    await event.reply(f"Error: {e}")
        return

@bot.on(events.NewMessage(pattern='/forward'))
async def forward_command(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return
    await event.reply("How many messages per group? (1-5)")

@bot.on(events.NewMessage)
async def handle_forward(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        return

    try:
        count = int(event.text)
        if 1 <= count <= 5:
            await event.reply("How many rounds?")
        else:
            await event.reply("Invalid number. Choose between 1-5.")
            return
    except ValueError:
        return

    rounds = int((await bot.get_messages(event.chat_id, limit=1)).text)
    await event.reply("Enter delay between rounds (seconds):")
    delay = int((await bot.get_messages(event.chat_id, limit=1)).text)

    for file in os.listdir(CREDENTIALS_FOLDER):
        session_name = os.path.join(CREDENTIALS_FOLDER, file)
        user_client = TelegramClient(session_name, BOT_API_ID, BOT_API_HASH)
        await user_client.connect()

        for _ in range(rounds):
            async for dialog in user_client.iter_dialogs():
                if dialog.is_group:
                    try:
                        await user_client.send_message(dialog.entity, "Ad message here!")
                        await asyncio.sleep(random.uniform(2, 4))
                    except FloodWaitError as e:
                        await asyncio.sleep(e.seconds)
            await asyncio.sleep(delay)

print("Bot is running...")
bot.start(bot_token=BOT_API_TOKEN)
bot.run_until_disconnected()
