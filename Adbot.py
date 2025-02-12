import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import init
import random
from pymongo import MongoClient

# Initialize colorama for colored output
init(autoreset=True)

# Replace with your API credentials
USER_API_ID = "26416419"
USER_API_HASH = "c109c77f5823c847b1aeb7fbd4990cc4"
BOT_API_TOKEN = "7226701592:AAFl69s6ea_yi24FrXpVN8FmznwCM7-alao"

CREDENTIALS_FOLDER = 'sessions'

# MongoDB connection
MONGO_URI = "mongodb+srv://admin22:admin22@cluster0.9lqp0ci.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["autobot"]
allowed_users_collection = db["allowed_users"]

# Ensure session folder exists
if not os.path.exists(CREDENTIALS_FOLDER):
    os.mkdir(CREDENTIALS_FOLDER)

# Initialize Telegram bot
bot = TelegramClient('bot_session', USER_API_ID, USER_API_HASH)

# Define the bot owner
OWNER_ID = 6748827895  # Replace with the owner user ID

# Function to get allowed users from MongoDB
def get_allowed_users():
    users = set()
    for user in allowed_users_collection.find():
        users.add(user["user_id"])
    return users

# Load allowed users and ensure owner is always authorized
ALLOWED_USERS = get_allowed_users()
ALLOWED_USERS.add(OWNER_ID)

# Ensure the owner is in the database
if not allowed_users_collection.find_one({"user_id": OWNER_ID}):
    allowed_users_collection.insert_one({"user_id": OWNER_ID})

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    """Welcome message for users."""
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this bot.")
        return
    
    await event.reply("Welcome! Use the following commands:\n\n"
                      "/host - Host a new Telegram account\n"
                      "/forward - Start forwarding ads\n"
                      "/accounts - List hosted accounts\n"
                      "/remove - Remove a hosted account\n"
                      "/add {user_id} - Add a user to the allowed list (owner only)")

@bot.on(events.NewMessage(pattern='/add'))
async def add_command(event):
    """Adds a user to the allowed list."""
    user_id = event.sender_id
    if user_id != OWNER_ID:
        await event.reply("You are not authorized to use this command.")
        return

    user_input = event.text.split()
    if len(user_input) != 2:
        await event.reply("Usage: /add {user_id}")
        return

    new_user_id = int(user_input[1])
    if not allowed_users_collection.find_one({"user_id": new_user_id}):
        allowed_users_collection.insert_one({"user_id": new_user_id})
        ALLOWED_USERS.add(new_user_id)
        await event.reply(f"User {new_user_id} added to the allowed list.")
    else:
        await event.reply("User is already in the allowed list.")

@bot.on(events.NewMessage(pattern='/host|/addaccount'))
async def host_command(event):
    """Starts the hosting process for a new account."""
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return

    await event.reply("Send your API ID, API Hash, and phone number in the format:\n`API_ID|API_HASH|PHONE_NUMBER`")

@bot.on(events.NewMessage)
async def process_input(event):
    """Processes user input for account hosting."""
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        return

    data = event.text.split('|')
    if len(data) == 3:
        api_id, api_hash, phone_number = data
        session_name = f"{CREDENTIALS_FOLDER}/session_{user_id}_{phone_number}"
        client = TelegramClient(session_name, api_id, api_hash)

        try:
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                await event.reply("OTP sent to your phone. Reply with the OTP.")
            else:
                await event.reply(f"Account {phone_number} is already authorized and hosted!")
        except Exception as e:
            await event.reply(f"Error: {e}")

    elif event.text.isdigit():
        otp = event.text.strip()
        try:
            client.sign_in(phone_number, otp)
            await event.reply(f"Account {phone_number} successfully hosted!")
        except Exception as e:
            await event.reply(f"Error: {e}")

@bot.on(events.NewMessage(pattern='/forward'))
async def forward_command(event):
    """Starts the ad forwarding process."""
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return

    await event.reply("Enter how many messages you want to forward per group (1-5):")

@bot.on(events.NewMessage)
async def forward_ads(event):
    """Handles forwarding ads."""
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        return

    try:
        message_count = int(event.text.strip())
        if 1 <= message_count <= 5:
            await event.reply("How many rounds of ads would you like to run?")
        else:
            await event.reply("Please choose a number between 1 and 5.")
    except ValueError:
        return

    rounds = int(event.text.strip())
    await event.reply("Enter delay (in seconds) between rounds.")
    
    delay = int(event.text.strip())
    await event.reply("Starting the ad forwarding process...")

    for round_num in range(1, rounds + 1):
        async for dialog in bot.iter_dialogs():
            if dialog.is_group:
                group = dialog.entity
                try:
                    await bot.send_message(group.id, "Ad message here!")
                    await asyncio.sleep(random.uniform(2, 4))
                except FloodWaitError as e:
                    print(f"Rate limited. Waiting for {e.seconds} seconds.")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print(f"Failed to forward to {group.title}: {e}")
        if round_num < rounds:
            await asyncio.sleep(delay)

print("Bot is running...")
bot.start(bot_token=BOT_API_TOKEN)
bot.run_until_disconnected()
