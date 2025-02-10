from Devine import devine as app
from config import HANDLER
from pyrogram import filters, errors
from Devine.Database.gmutedb import get_gmuted_users, gmute_user, ungmute_user
from Devine.helpers.help_func import get_arg
from Devine.helpers.utils import CheckAdmin


@app.on_message(filters.command("gmute", HANDLER) & filters.me)
async def gmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            return await message.edit("**ᴡʜᴏᴍ sʜᴏᴜʟᴅ ɪ ɢᴍᴜᴛᴇ?**")
    
    try:
        get_user = await app.get_users(user)
        await gmute_user(get_user.id)
        await message.edit(f"**ɢʟᴏʙᴀʟʟʏ ᴍᴜᴛᴇᴅ {get_user.first_name}, ʟᴏʟ!**")
    except errors.RPCError as e:
        await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@app.on_message(filters.command("ungmute", HANDLER) & filters.me)
async def ungmute(_, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user.id
    else:
        user = get_arg(message)
        if not user:
            return await message.edit("**ᴡʜᴏᴍ sʜᴏᴜʟᴅ ɪ ᴜɴɢᴍᴜᴛᴇ?**")
    
    try:
        get_user = await app.get_users(user)
        await ungmute_user(get_user.id)
        await message.edit(f"**ᴜɴᴍᴜᴛᴇᴅ {get_user.first_name}, ᴇɴᴊᴏʏ!**")
    except errors.RPCError as e:
        await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@app.on_message(filters.group & filters.incoming)
async def check_and_del(_, message):
    if not message or not message.from_user:
        return

    try:
        gmuted_users = await get_gmuted_users()
        if message.from_user.id not in gmuted_users:
            return
    except AttributeError:
        return

    try:
        await app.delete_messages(message.chat.id, message.message_id)
    except errors.RPCError:
        pass  # Bot might not have delete permissions
