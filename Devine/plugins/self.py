import os
from pyrogram import Client, filters
from pyrogram.types import Message
from Devine import devine
from config import HANDLER

@devine.on_message(filters.command("msave", HANDLER) & filters.me)
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media

    if not media:
        await message.edit("<b>ᴍᴇᴅɪᴀ ɪs ʀᴇǫᴜɪʀᴇᴅ</b>")
        return
    await message.delete()

    try:
        path = await message.reply_to_message.download()
    except Exception as e:
        await message.reply(f"<b>ᴇʀʀᴏʀ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴍᴇᴅɪᴀ:</b> <code>{str(e)}</code>")
        return

    if media.type == "photo":
        try:
            await client.send_photo("me", path)
        except Exception as e:
            await message.reply(f"<b>ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴘʜᴏᴛᴏ:</b> <code>{str(e)}</code>")
    elif media.type == "video":
        try:
            await client.send_video("me", path)
        except Exception as e:
            await message.reply(f"<b>ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴠɪᴅᴇᴏ:</b> <code>{str(e)}</code>")
    elif media.type == "document":
        try:
            await client.send_document("me", path)
        except Exception as e:
            await message.reply(f"<b>ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴅᴏᴄᴜᴍᴇɴᴛ:</b> <code>{str(e)}</code>")

    os.remove(path)
