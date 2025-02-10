from config import HANDLER, OWNER_ID
from Devine import devine as app, MODULE
import os
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied

infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    " > ᴜsᴇʀ ɪᴅ: `{user_id}`\n"
    " > ɴᴀᴍᴇ: `{first_name}`\n"
    " > ʟᴀsᴛ ɴᴀᴍᴇ: `{last_name}`\n"
    " > ᴜsᴇʀɴᴀᴍᴇ: {username}\n"
    " > ᴅᴀᴛᴀ ᴄᴇɴᴛᴇʀ: {dc_id}\n"
    " > sᴛᴀᴛᴜs: {status}\n"
    " > sᴄᴀᴍ: {scam}\n"
    " > ʙᴏᴛ: {bot}\n"
    " > ᴠᴇʀɪғɪᴇᴅ: {verified}\n"
    " > ᴄᴏɴᴛᴀᴄᴛ: {contact}\n"
    " > ᴄᴏᴍᴍᴏɴ ɢʀᴏᴜᴘs: {common}"
)

@app.on_message(filters.command("whois", HANDLER) & filters.me)
async def whois(client, message: Message):
    cmd = message.command
    target_user = None

    if message.reply_to_message:
        target_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        target_user = cmd[1]
        if target_user.isdigit():
            target_user = int(target_user)
    
    if not target_user:
        target_user = message.from_user.id  # Default to self if no target

    try:
        user = await client.get_users(target_user)
    except (PeerIdInvalid, UsernameNotOccupied):
        return await message.reply("• ɪ ᴄᴀɴ'ᴛ ғɪɴᴅ ᴛʜᴀᴛ ᴜsᴇʀ.")
    
    common = await app.get_common_chats(user.id)
    
    # Get profile picture if available
    pfp = None
    if user.photo:
        pfp = await client.download_media(user.photo.big_file_id)

    await message.delete()

    caption_text = infotext.format(
        full_name=user.first_name + (" " + user.last_name if user.last_name else ""),
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name or "N/A",
        username=f"@{user.username}" if user.username else "N/A",
        dc_id=user.dc_id if hasattr(user, "dc_id") else "N/A",
        status=user.status if hasattr(user, "status") else "N/A",
        scam="✔" if user.is_scam else "✘",
        bot="✔" if user.is_bot else "✘",
        verified="✔" if user.is_verified else "✘",
        contact="✔" if user.is_contact else "✘",
        common=len(common),
    )

    if pfp:
        await app.send_photo(
            message.chat.id,
            photo=pfp,
            caption=caption_text,
            reply_to_message_id=message.reply_to_message.id if message.reply_to_message else None,
        )
        os.remove(pfp)  # Safe file deletion
    else:
        await message.reply(caption_text, quote=True)


@app.on_message(filters.command("id", HANDLER) & filters.me)
async def getid(client, message: Message):
    chat = message.chat
    reply = message.reply_to_message
    text = ""

    if not reply and len(message.command) == 1:
        text = f"ᴛʜɪs ᴄʜᴀᴛ's ɪᴅ ɪs : `<code>{chat.id}</code>`\n"

    elif reply and not reply.forward_from_chat and not reply.sender_chat:
        user_id = reply.from_user.id
        first_name = reply.from_user.first_name
        text = f"ᴜsᴇʀ {first_name}'s ɪᴅ ɪs `<code>{user_id}</code>`.\n"

    elif reply and reply.forward_from_chat:
        user_id = reply.from_user.id
        first_name = reply.from_user.first_name
        channel_id = reply.forward_from_chat.id
        channel_title = reply.forward_from_chat.title
        text = (
            f"ᴜsᴇʀ {first_name}'s ɪᴅ ɪs `<code>{user_id}</code>`.\n"
            f"ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀɴɴᴇʟ, {channel_title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `<code>{channel_id}</code>`.\n\n"
        )

    elif reply and reply.sender_chat:
        chat_id = reply.sender_chat.id
        chat_title = reply.sender_chat.title
        text = f"ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴄʜᴀᴛ/ᴄʜᴀɴɴᴇʟ, {chat_title}, ʜᴀs ᴀɴ ɪᴅ ᴏғ `<code>{chat_id}</code>`."

    elif len(message.command) == 2 and message.command[1].startswith('@'):
        username = message.command[1][1:]  # Remove the '@' symbol
        try:
            user = await client.get_users(username)
            text = f"ᴜsᴇʀ {user.first_name}'s ɪᴅ ɪs `<code>{user.id}</code>`."
        except UsernameNotOccupied:
            text = "ᴛʜᴇ ᴜsᴇʀɴᴀᴍᴇ ɪs ɴᴏᴛ ᴏᴄᴄᴜᴘɪᴇᴅ."

    await message.reply_text(text, disable_web_page_preview=True)


