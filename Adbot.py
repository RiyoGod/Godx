import os
import asyncio
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import init
import random
from pymongo import MongoClient

# Initialize colorama for colored output
init(autoreset=True)

# MongoDB Configuration
MONGO_URI = "mongodb+srv://admin22:admin22@cluster0.9lqp0ci.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"  # Change if needed
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["AutoBotDB"]

# Collections
accounts_col = db["accounts"]
users_col = db["allowed_users"]

# Replace with your API credentials
USER_API_ID = "26416419"
USER_API_HASH = "c109c77f5823c847b1aeb7fbd4990cc4"
BOT_API_TOKEN = "7226701592:AAFl69s6ea_yi24FrXpVN8FmznwCM7-alao"

# Initialize Telegram bot
bot = TelegramClient('bot_session', USER_API_ID, USER_API_HASH)

# Define the bot owner
OWNER_ID = 6748827895  # Replace with your user ID

# Get allowed users from MongoDB
def get_allowed_users():
    return {doc["user_id"] for doc in users_col.find()}

ALLOWED_USERS = get_allowed_users()

# Store user states
user_states = {}

# Dictionary to store hosted accounts
accounts = {}

# /start command
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
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

# /add command to add allowed users (owner only)
@bot.on(events.NewMessage(pattern='/add'))
async def add_command(event):
    user_id = event.sender_id
    if user_id != OWNER_ID:
        await event.reply("You are not authorized to use this command.")
        return

    user_input = event.text.split()
    if len(user_input) != 2:
        await event.reply("Usage: /add {user_id}")
        return

    new_user_id = int(user_input[1])
    if users_col.find_one({"user_id": new_user_id}):
        await event.reply(f"User {new_user_id} is already in the allowed list.")
    else:
        users_col.insert_one({"user_id": new_user_id})
        ALLOWED_USERS.add(new_user_id)
        await event.reply(f"User {new_user_id} added to the allowed list.")

# /host command to add a new Telegram account
@bot.on(events.NewMessage(pattern='/host'))
async def host_command(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return

    user_states[user_id] = {'step': 'awaiting_credentials'}
    await event.reply("Send your API ID, API Hash, and phone number in the format:\n`API_ID|API_HASH|PHONE_NUMBER`")

@bot.on(events.NewMessage)
async def process_input(event):
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state['step'] == 'awaiting_credentials':
        data = event.text.split('|')
        if len(data) != 3:
            await event.reply("Invalid format. Please send data as:\n`API_ID|API_HASH|PHONE_NUMBER`")
            return

        api_id, api_hash, phone_number = data
        session_name = f"session_{phone_number}"
        client = TelegramClient(session_name, api_id, api_hash)

        try:
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(phone_number)
                state.update({'step': 'awaiting_otp', 'client': client, 'phone_number': phone_number})
                await event.reply("OTP sent to your phone. Reply with the OTP.")
            else:
                accounts_col.insert_one({
                    "phone_number": phone_number,
                    "api_id": api_id,
                    "api_hash": api_hash,
                    "session": session_name
                })
                accounts[phone_number] = client
                await client.disconnect()
                await event.reply(f"Account {phone_number} hosted successfully!")
                del user_states[user_id]
        except Exception as e:
            await event.reply(f"Error: {e}")
            del user_states[user_id]

    elif state['step'] == 'awaiting_otp':
        otp = event.text.strip()
        client = state['client']
        phone_number = state['phone_number']

        try:
            await client.sign_in(phone_number, otp)
            accounts_col.insert_one({
                "phone_number": phone_number,
                "api_id": client.api_id,
                "api_hash": client.api_hash,
                "session": f"session_{phone_number}"
            })
            accounts[phone_number] = client
            await event.reply(f"Account {phone_number} successfully hosted!")
            del user_states[user_id]
        except Exception as e:
            await event.reply(f"Error: {e}")
            del user_states[user_id]

# /accounts command to list hosted accounts
@bot.on(events.NewMessage(pattern='/accounts'))
async def list_accounts(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return

    hosted_accounts = list(accounts_col.find({}, {"_id": 0, "phone_number": 1}))
    if not hosted_accounts:
        await event.reply("No accounts are hosted.")
    else:
        account_list = '\n'.join([acc["phone_number"] for acc in hosted_accounts])
        await event.reply(f"Hosted accounts:\n{account_list}")

# /remove command to delete a hosted account
@bot.on(events.NewMessage(pattern='/remove'))
async def remove_account(event):
    user_id = event.sender_id
    if user_id not in ALLOWED_USERS:
        await event.reply("You are not authorized to use this command.")
        return

    user_states[user_id] = {'step': 'awaiting_account_removal'}
    await event.reply("Send the phone number of the account you want to remove.")

@bot.on(events.NewMessage)
async def process_removal(event):
    user_id = event.sender_id
    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state['step'] == 'awaiting_account_removal':
        phone_number = event.text.strip()
        account = accounts_col.find_one({"phone_number": phone_number})

        if not account:
            await event.reply("Account not found.")
        else:
            accounts_col.delete_one({"phone_number": phone_number})
            accounts.pop(phone_number, None)
            await event.reply(f"Account {phone_number} removed successfully.")
        del user_states[user_id]

# Run the bot
print("Bot is running...")
bot.start(bot_token=BOT_API_TOKEN)
bot.run_until_disconnected()
