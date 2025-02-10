from pyrogram import filters
from pyrogram.types import Message
import requests
import config
from Devine import devine

@devine.on_message(filters.me & filters.command("write", prefixes=config.HANDLER))
async def handwriting(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("• ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴡʀɪᴛᴇ...")
    
    m = await message.reply_text("• ɪ'ᴍ ᴡʀɪᴛɪɴɢ, ᴡᴀɪᴛ...")
    text = message.text.split(None, 1)[1].replace(" ", "%20")
    api_url = f"https://apis.xditya.me/write?text={text}"
    
    try:
        response = requests.get(api_url)
        if response.status_code != 200:
            return await m.edit("• ғᴀɪʟᴇᴅ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴛʜᴇ ɪᴍᴀɢᴇ.")
        
        image_url = response.url
        await m.edit("• ᴜᴘʟᴏᴀᴅɪɴɢ...")
        await m.delete()
        await message.reply_photo(image_url)

    except Exception as e:
        await m.edit(f"• ᴇʀʀᴏʀ: {str(e)}")

    await message.delete()  
