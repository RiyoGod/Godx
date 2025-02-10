import config
from Devine import devine as app
from pyrogram import filters
from pyrogram.types import Message

HELP_TEXT = """ 
```ᴍᴏᴅᴇʀᴀᴛɪᴏɴ
• `.unbanall` – ᴜɴʙᴀɴs ᴀʟʟ ᴘʀᴇᴠɪᴏᴜsʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ɪɴ ᴀ ɢʀᴏᴜᴘ.
• `.banall` – ʙᴀɴs ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ.
• `.kickall` – ᴋɪᴄᴋs ᴀʟʟ ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴀ ɢʀᴏᴜᴘ.
• `.ban` – ʙᴀɴs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ.
• `.unban` – ᴜɴʙᴀɴs ᴀ ᴜsᴇʀ ғʀᴏᴍ ᴛʜᴇ ᴄʜᴀᴛ.
• `.purge` – ᴅᴇʟᴇᴛᴇs ᴍᴜʟᴛɪᴘʟᴇ ᴍᴇssᴀɢᴇs.
• `.del` – ᴅᴇʟᴇᴛᴇs ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.

ᴀᴅᴍɪɴ
• `.promote` – ɢʀᴀɴᴛs ᴀᴅᴍɪɴ ᴘʀɪᴠɪʟᴇɢᴇs ᴛᴏ ᴀ ᴜsᴇʀ.
• `.fpromote` – ғᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇs ᴀ ᴜsᴇʀ.
• `.pin` – ᴘɪɴs ᴀ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.
• `.unpin` – ᴜɴᴘɪɴs ᴀ ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ.
• `.admins` – ʟɪsᴛs ᴀʟʟ ᴀᴅᴍɪɴs ɪɴ ᴛʜᴇ ᴄʜᴀᴛ.
• `.invite` – ɢᴇɴᴇʀᴀᴛᴇs ᴀɴ ɪɴᴠɪᴛᴇ ʟɪɴᴋ.

ᴜᴛɪʟɪᴛɪᴇs
• `.ud` <ᴡᴏʀᴅ> – ғᴇᴛᴄʜᴇs ᴛʜᴇ ᴅᴇғɪɴɪᴛɪᴏɴ ғʀᴏᴍ ᴜʀʙᴀɴ ᴅɪᴄᴛɪᴏɴᴀʀʏ.
• `.tr` <ʟᴀɴɢ_ᴄᴏᴅᴇ> – ᴛʀᴀɴsʟᴀᴛᴇs ᴀ ᴍᴇssᴀɢᴇ.
• `.afk` – sᴇᴛs ʏᴏᴜʀ sᴛᴀᴛᴜs ᴛᴏ ᴀғᴋ.

ᴘᴍ ɢᴜᴀʀᴅ
• `.pmguard` ᴏɴ/ᴏғғ – ᴇɴᴀʙʟᴇs ᴏʀ ᴅɪsᴀʙʟᴇs ᴘᴍ ɢᴜᴀʀᴅ.
• `.setlimit` <ɴᴜᴍʙᴇʀ> – sᴇᴛs ᴡᴀʀɴɪɴɢ ʟɪᴍɪᴛ.
• `.setpmmsg` <ᴍᴇssᴀɢᴇ> – sᴇᴛs ᴘᴍ ᴡᴀʀɴɪɴɢ ᴍᴇssᴀɢᴇ.
• `.setblockmsg` <ᴍᴇssᴀɢᴇ> – sᴇᴛs ʙʟᴏᴄᴋ ᴍᴇssᴀɢᴇ.
• `.allow` – ᴀʟʟᴏᴡs ᴘᴍs.
• `.deny` – ᴅᴇɴɪᴇs ᴘᴍs.

ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ
• `.run` <ᴄᴏᴅᴇ> / `.eval` <ᴄᴏᴅᴇ> – ᴇxᴇᴄᴜᴛᴇs ᴘʏᴛʜᴏɴ ᴄᴏᴅᴇ.
• `.sh` <ᴄᴏᴍᴍᴀɴᴅ> / `.shell` <ᴄᴏᴍᴍᴀɴᴅ> – ʀᴜɴs sʜᴇʟʟ ᴄᴏᴍᴍᴀɴᴅs.

ᴛᴏᴏʟs
• `.weather` – ɢᴇᴛs ᴡᴇᴀᴛʜᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ.
• `.carbon` – ɢᴇɴᴇʀᴀᴛᴇs ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇ.
• `.upscale` – ᴜᴘsᴄᴀʟᴇs ᴀɴ ɪᴍᴀɢᴇ.
• `.tgm` – ᴜᴘʟᴏᴀᴅs ᴘʜᴏᴛᴏs ᴛᴏ ᴛᴇʟᴇɢʀᴀᴘʜ.
• `.shelp` – sᴇɴᴅs ᴀ ᴅᴇʟᴀʏᴇᴅ sᴘᴀᴍ ᴍᴇssᴀɢᴇ.```
"""

@app.on_message(filters.command(["menu", "help"], prefixes=config.HANDLER) & filters.me)
async def menu_command(_, message: Message):
    await message.edit_text(HELP_TEXT)
