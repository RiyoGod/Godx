import requests
import time
import asyncio
from pyrogram import filters
from Devine import devine, MODULE
from config import HANDLER

CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"
MAX_FILE_SIZE_MB = 50  

async def send_temp_message(message, text):
    reply = await message.reply(text)
    for i in range(3):
        await asyncio.sleep(0.3)  
        updated_text = text + '.' * (i + 1)  
        await reply.edit(updated_text)  
    return reply  

async def upload_to_catbox(message, file_path):
    waiting_message = await send_temp_message(message, "ᴡᴀɪᴛ")  
    start_time = time.time()

    with open(file_path, 'rb') as file:
        response = requests.post(
            CATBOX_UPLOAD_URL,
            data={"reqtype": "fileupload"},
            files={"fileToUpload": file}
        )

    upload_time = round(time.time() - start_time, 2)

    if response.status_code == 200 and response.text.startswith("https://"):
        file_url = response.text.strip()
        await waiting_message.edit(f"<b>ᴜᴘʟᴏᴀᴅᴇᴅ ᴛᴏ ᴄᴀᴛʙᴏx ɪɴ {upload_time} sᴇᴄᴏɴᴅs:</b>\n\n<a href='{file_url}'>{file_url}</a>")
    else:
        await waiting_message.edit("<b>ғᴀɪʟᴇᴅ ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ғɪʟᴇ.</b>")

async def handle_upload(client, message, target_message):
    media = target_message.photo or target_message.video or target_message.document
    if not media:
        return await message.reply("<b>sᴇɴᴅ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ, ᴠɪᴅᴇᴏ, ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.</b>")

    file_size = media.file_size / (1024 * 1024)  
    if file_size > MAX_FILE_SIZE_MB:
        return await message.reply("<b>ғɪʟᴇ sɪᴢᴇ ᴇxᴄᴇᴇᴅs 50 ᴍʙ ʟɪᴍɪᴛ.</b>")

    file_path = await target_message.download()
    await upload_to_catbox(message, file_path)  

@devine.on_message(filters.command("tgm", prefixes=HANDLER) & filters.me)
async def upload_command(client, message):
    if message.from_user.is_bot:
        return  

    target_message = message.reply_to_message if message.reply_to_message else message
    await handle_upload(client, message, target_message)

__mod__ = "TGM"  
__help__ = """  
• /tgm - ᴜᴘʟᴏᴀᴅ ᴘʜᴏᴛᴏs ᴀɴᴅ ғɪʟᴇs ᴛᴏ ᴄᴀᴛʙᴏx.
"""  

MODULE.append({"module": __mod__, "help": __help__})
