from pyrogram import filters
from pyrogram.errors import FloodWait
import asyncio
from Devine import devine
from config import OWNER_ID, HANDLER


@devine.on_message(filters.command("leave", prefixes=HANDLER) & filters.me)
async def leave_chat(_, message):
    try:
        if len(message.command) > 1:
            group_id = int(message.command[1])
            await devine.send_message(group_id, "**ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛ...**")
            msg = await message.reply_text("**ʟᴇᴀᴠɪɴɢ ᴄʜᴀᴛ ɪɴ 𝟸 sᴇᴄ...**")
            await message.delete()
            await asyncio.sleep(2)
            await msg.edit("**ᴄʜᴀᴛ ʟᴇғᴛ sᴜᴄᴄᴇssғᴜʟʟʏ**")
            await devine.leave_chat(group_id)
        else:
            msg = await message.reply_text("**ʟᴇᴀᴠɪɴɢ ᴄᴜʀʀᴇɴᴛ ᴄʜᴀᴛ ɪɴ 𝟸 sᴇᴄ...**")
            await message.delete()
            await asyncio.sleep(2)
            await msg.edit("**ᴄʜᴀᴛ ʟᴇғᴛ**")
            await devine.leave_chat(message.chat.id)

    except FloodWait as e:
        await asyncio.sleep(e.value)
        await message.reply_text("**ᴛʀʏɪɴɢ ᴀɢᴀɪɴ ᴅᴜᴇ ᴛᴏ ʀᴀᴛᴇ ʟɪᴍɪᴛs...**")
        await leave_chat(_, message)

    except Exception as e:
        await message.reply_text(
            f"**ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`\n\n• **ᴍᴀɴᴜᴀʟʟʏ ʀᴇᴍᴏᴠᴇ ᴍᴇ ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ.**"
        )
