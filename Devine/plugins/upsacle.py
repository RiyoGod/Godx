import os
from pyrogram import filters
from pyrogram.types import Message
from Devine import devine as app
from lexica import Client as LexicaClient
from config import HANDLER

async def getFile(message: Message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.photo:
        return await message.reply_to_message.download()
    elif (
        message.reply_to_message.document 
        and message.reply_to_message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg']
    ):
        return await message.reply_to_message.download()
    return None

async def UpscaleImages(image: bytes) -> str:
    try:
        client = LexicaClient()
        content = client.upscale(image)  # Ensure LexicaClient supports this method
        
        upscaled_file_path = "upscaled.png"
        with open(upscaled_file_path, "wb") as output_file:
            output_file.write(content)
        
        return upscaled_file_path
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")

@app.on_message(filters.command("upscale", prefixes=HANDLER) & filters.me)
async def upscaleImages(_, message: Message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ.")
    
    msg = await message.reply("ᴜᴘsᴄᴀʟɪɴɢ...")

    with open(file, "rb") as f:
        imageBytes = f.read()
    os.remove(file)
    
    try:
        upscaledImage = await UpscaleImages(imageBytes)
        await message.reply_document(upscaledImage)
        await msg.delete()
        os.remove(upscaledImage)
    except Exception as e:
        await msg.edit(f"Failed to upscale the image: {e}")
