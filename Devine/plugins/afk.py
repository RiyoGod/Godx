import time
import asyncio
from pyrogram import Client, filters
from Devine import devine
from Devine.helpers.help_func import get_arg, user_afk, get_datetime
import Devine.Database.afk_db as Zect
from Devine import get_readable_time
from Devine.helpers.utils import get_message_type, Types
from config import HANDLER, OWNER_ID, GROUP_ID

MENTIONED = []
AFK_RESTRICT = {}
DELAY_TIME = 20


@devine.on_message(filters.command("afk", HANDLER) & filters.me)
async def afk(_, message):
    afk_time = int(time.time())
    reason = get_arg(message) or None
    await Zect.set_afk(True, afk_time, reason)
    await message.edit("**ɪ'ᴍ ɢᴏɪɴɢ ᴀғᴋ**")


@devine.on_message(filters.mentioned & ~filters.bot & filters.create(user_afk), group=11)
async def afk_mentioned(_, message):
    global MENTIONED, AFK_RESTRICT
    afk_time, reason = await Zect.afk_stuff()
    afk_since = get_readable_time(time.time() - afk_time)

    chat_id = str(message.chat.id).lstrip("-100")
    current_time = int(time.time())

    if chat_id in AFK_RESTRICT and current_time < AFK_RESTRICT[chat_id]:
        return
    AFK_RESTRICT[chat_id] = current_time + DELAY_TIME

    reply_text = f"**ɪ'ᴍ ᴀғᴋ ʀɪɢʜᴛ ɴᴏᴡ (sɪɴᴄᴇ {afk_since})**"
    if reason:
        reply_text += f"\n• **ʀᴇᴀsᴏɴ:** __{reason}__"

    await message.reply(reply_text)

    _, message_type = get_message_type(message)
    text = message.text or message.caption if message_type == Types.TEXT else message_type.name

    MENTIONED.append(
        {
            "user": message.from_user.first_name,
            "user_id": message.from_user.id,
            "chat": message.chat.title or "Private",
            "chat_id": chat_id,
            "text": text[:50] + "..." if len(text) > 50 else text,
            "message_id": message.message_id,
        }
    )


@devine.on_message(filters.create(user_afk) & filters.outgoing)
async def auto_unafk(_, message):
    global MENTIONED
    await Zect.set_unafk()
    unafk_message = await devine.send_message(message.chat.id, "**ɪ'ᴍ ɴᴏ ʟᴏɴɢᴇʀ ᴀғᴋ**")

    if MENTIONED:
        text = "**ᴛᴏᴛᴀʟ {} ᴍᴇɴᴛɪᴏɴᴇᴅ ʏᴏᴜ**\n".format(len(MENTIONED))
        for x in MENTIONED:
            text += "- [{}](https://t.me/c/{}/{}) ({}): {}\n".format(
                x["user"], x["chat_id"], x["message_id"], x["chat"], x["text"]
            )
        await devine.send_message(GROUP_ID, text)
        MENTIONED = []

    await asyncio.sleep(2)
    await unafk_message.delete()
