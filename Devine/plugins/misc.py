import asyncio
import requests
from gpytranslate import Translator
from pyrogram import filters
from Devine import devine, MODULE
from config import HANDLER

@devine.on_message(filters.command(["ud", "define"], prefixes=HANDLER) & filters.me)
async def ud(_, message):
    if len(message.command) < 2:
        return await message.edit("**ᴡʜᴇʀᴇ ʏᴏᴜ ɪɴᴘᴜᴛ ᴛʜᴇ ᴛᴇxᴛ?**")
    
    text = message.text.split(None, 1)[1]
    
    try:
        results = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
        reply_text = f"**ʀᴇsᴜʟᴛs: {text}**\n\n{results['list'][0]['definition']}\n\n_{results['list'][0]['example']}_"
    except Exception as e:
        return await message.edit_text(f"**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ:**\n`{e}`")
    
    ud = await message.edit_text("**ᴇxᴘʟᴏʀɪɴɢ...**")
    await ud.edit_text(reply_text)


trans = Translator()

@devine.on_message(filters.command("tr", prefixes=HANDLER) & filters.me)
async def translate(_, message):
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("**[ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴜsɪɴɢ ᴛʜᴇ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇ ᴘʀᴏᴠɪᴅᴇᴅ!](https://telegra.ph/Lang-Codes-03-19-3)**")
        return

    to_translate = reply_msg.text or reply_msg.caption

    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source, dest = args.split("//")
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"

    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"**ᴛʀᴀɴsʟᴀᴛᴇᴅ ᴛʀᴏᴍ {source} ᴛᴏ {dest}**:\n`{translation.text}`"

    await message.delete()
    await reply_msg.reply_text(reply)
