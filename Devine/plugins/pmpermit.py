from pyrogram import filters
import asyncio
from Devine import devine 
from Devine.helpers.help_func import get_arg, denied_users
import Devine.Database.pm_db as Zectdb
from config import HANDLER

FLOOD_CTRL = 0
USERS_AND_WARNS = {}

@devine.on_message(filters.command("pmguard", HANDLER) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("<b>ɪ ᴏɴʟʏ ᴜɴᴅᴇʀsᴛᴀɴᴅ <code>ᴏɴ</code> ᴏʀ <code>ᴏғғ</code></b>")
        return
    if arg == "off":
        await Zectdb.set_pm(False)
        await message.edit("<b>ᴘᴍ ɢᴜᴀʀᴅ ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ</b>")
    if arg == "on":
        await Zectdb.set_pm(True)
        await message.edit("<b>ᴘᴍ ɢᴜᴀʀᴅ ᴀᴄᴛɪᴠᴀᴛᴇᴅ</b>")

@devine.on_message(filters.command("setlimit", HANDLER) & filters.me)
async def setlimit(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("<b>sᴇᴛ ʟɪᴍɪᴛ ᴛᴏ ᴡʜᴀᴛ?</b>")
        return
    await Zectdb.set_limit(int(arg))
    await message.edit(f"<b>ʟɪᴍɪᴛ sᴇᴛ ᴛᴏ <code>{arg}</code></b>")

@devine.on_message(filters.command("setpmmsg", HANDLER) & filters.me)
async def setpmmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("<b>ᴡʜᴀᴛ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇᴛ?</b>")
        return
    if arg == "default":
        await Zectdb.set_permit_message(Zectdb.PMPERMIT_MESSAGE)
        await message.edit("<b>ᴀɴᴛɪ-ᴘᴍ ᴍᴇssᴀɢᴇ sᴇᴛ ᴛᴏ ᴅᴇғᴀᴜʟᴛ.</b>")
        return
    await Zectdb.set_permit_message(f"`{arg}`")
    await message.edit("<b>ᴄᴜsᴛᴏᴍ ᴀɴᴛɪ-ᴘᴍ ᴍᴇssᴀɢᴇ sᴇᴛ.</b>")

@devine.on_message(filters.command("setblockmsg", HANDLER) & filters.me)
async def setblockmsg(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("<b>ᴡʜᴀᴛ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇᴛ?</b>")
        return
    if arg == "default":
        await Zectdb.set_block_message(Zectdb.BLOCKED)
        await message.edit("<b>ʙʟᴏᴄᴋ ᴍᴇssᴀɢᴇ sᴇᴛ ᴛᴏ ᴅᴇғᴀᴜʟᴛ.</b>")
        return
    await Zectdb.set_block_message(f"`{arg}`")
    await message.edit("<b>ᴄᴜsᴛᴏᴍ ʙʟᴏᴄᴋ ᴍᴇssᴀɢᴇ sᴇᴛ.</b>")

@devine.on_message(filters.command("allow", HANDLER) & filters.me & filters.private)
async def allow(client, message):
    chat_id = message.chat.id
    await Zectdb.allow_user(chat_id)
    await message.edit(f"<b>ɪ ʜᴀᴠᴇ ᴀʟʟᴏᴡᴇᴅ [ʏᴏᴜ](tg://user?id={chat_id}) ᴛᴏ ᴘᴍ ᴍᴇ.</b>")
    async for msg in devine.search_messages(chat_id=chat_id, query=Zectdb.PMPERMIT_MESSAGE, limit=1, from_user="me"):
        await msg.delete()
    USERS_AND_WARNS.update({chat_id: 0})

@devine.on_message(filters.command("deny", HANDLER) & filters.me & filters.private)
async def deny(client, message):
    chat_id = message.chat.id
    await Zectdb.deny_user(chat_id)
    await message.edit(f"<b>ɪ ʜᴀᴠᴇ ᴅᴇɴɪᴇᴅ [ʏᴏᴜ](tg://user?id={chat_id}) ᴛᴏ ᴘᴍ ᴍᴇ.</b>")

@devine.on_message(
    filters.private
    & filters.create(denied_users)
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def reply_pm(client, message):
    global FLOOD_CTRL
    pmpermit, pm_message, limit, block_message = await Zectdb.get_pm_settings()
    user = message.from_user.id
    user_warns = USERS_AND_WARNS.get(user, 0)

    if user_warns <= limit - 2:
        user_warns += 1
        USERS_AND_WARNS[user] = user_warns
        if FLOOD_CTRL > 0:
            FLOOD_CTRL = 0
            return
        FLOOD_CTRL += 1

        async for msg in devine.search_messages(chat_id=message.chat.id, query=pm_message, limit=1, from_user="me"):
            await msg.delete()
        await message.reply(pm_message, disable_web_page_preview=True)
        return

    await message.reply(block_message, disable_web_page_preview=True)
    await devine.block_user(message.chat.id)
    USERS_AND_WARNS[user] = 0
