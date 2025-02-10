import time
import asyncio
import config
from config import HANDLER
from pyrogram import filters, __version__ as pyrover
from Devine import devine, get_readable_time, StartTime

async def alive():
    katsuki = "3.01"
    user = await devine.get_me()
    name = user.first_name
    username = user.username
    user_profile_link = f"https://t.me/{username}" if username else ""
    user_hyperlink = f"[{name}]({user_profile_link})" if user_profile_link else name
    dbhealth = "ᴡᴏʀᴋɪɴɢ"
    uptime = get_readable_time(time.time() - StartTime)
    ping_time = round((time.time() - StartTime) * 1000, 3)

    url = "https://files.catbox.moe/dndxpg.mp4"

    ALIVE_TEXT = f"""ɪ'ᴍ ᴀʟɪᴠᴇ ᴍᴀꜱᴛᴇʀ

⟐ <b>ᴠᴇʀꜱɪᴏɴ :</b> {katsuki}
⟐ <b>ᴜᴘᴛɪᴍᴇ :</b> {uptime}
⟐ <b>ᴘɪɴɢ :</b> {ping_time} ms
⟐ <b>ᴘʏᴛʜᴏɴ :</b> {pyrover}

<b>ᴘᴏᴡᴇʀᴇᴅ ʙʏ [ᴅᴇᴠɪɴᴇ ɴᴇᴛᴡᴏʀᴋ](devine_network.t.me)</b>"""

    return ALIVE_TEXT, url


@devine.on_message(filters.command("alive", prefixes=HANDLER) & filters.me)
async def chk_alive(_, message):
    msg = await message.reply_text("ᴄʜᴇᴄᴋɪɴɢ...")
    try:
        alive_text, photo_url = await alive()
        await msg.delete()
        await message.reply_video(
            photo_url,
            caption=alive_text
        )
    except Exception as e:
        print("Error:", e)
        await msg.edit("An error occurred while checking the status.")

    try:
        await message.delete()
    except:
        pass
