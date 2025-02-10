import sys
import io

from subprocess import getoutput as run
import traceback

import config, strings
import asyncio

from pyrogram import filters, enums
from Devine import bot, INFO , devine
from Devine.helpers.help_func import emoji_convert
from pyrogram.errors import MessageTooLong

OWNER_ID = config.OWNER_ID  # Ensure OWNER_ID is correctly set in config
SPAM = []

async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {l_}" for l_ in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
     if message.from_user.id != OWNER_ID:
         return  # Ignore if not owner

     user_id = message.from_user.id
     info = await INFO.devine()
     botlive = await emoji_convert(bot.is_connected)
     applive = await emoji_convert(devine.is_connected)
     name = info.first_name
     id = info.id
     
     if user_id in SPAM:
         return
     
     SPAM.append(user_id)
     await message.forward(config.GROUP_ID)
     mention = f"[{name}](tg://user?id={id})"
     await message.reply_text(
         text=strings.BOT_START.format(mention=mention, applive=applive, botlive=botlive),
         quote=True,
         parse_mode=enums.ParseMode.MARKDOWN,
     )
     await asyncio.sleep(20)
     SPAM.remove(user_id)


@bot.on_message(filters.command("e"))
async def eval(client, message):
    if message.from_user.id != OWNER_ID:
        return  # Ignore if not owner

    msg = await message.reply("ᴀɴᴀʟʏᴢɪɴɢ ᴄᴏᴅᴇ...")

    try:
        cmd = message.text.split(message.text.split()[0])[1]
    except:
         return await msg.reply("ᴄᴀɴ ʏᴏᴜ ɪɴᴘᴜᴛ ᴛʜᴇ ᴄᴏᴅᴇ ᴛᴏ ʀᴜɴ ᴍʏ ᴘʀᴏɢʀᴀᴍ?")

    reply_to_ = message.reply_to_message or message

    old_stderr, old_stdout = sys.stderr, sys.stdout
    redirected_output, redirected_error = io.StringIO(), io.StringIO()
    sys.stdout, sys.stderr = redirected_output, redirected_error
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()

    stdout, stderr = redirected_output.getvalue(), redirected_error.getvalue()
    sys.stdout, sys.stderr = old_stdout, old_stderr

    evaluation = exc or stderr or stdout or "sᴜᴄᴄᴇss"

    final_output = f"<b>ᴄᴏᴅᴇ</b>: <code>{cmd}</code>\n\n<b>ʀᴇsᴜʟᴛs</b>:\n<code>{evaluation.strip()}</code>\n"

    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to_.reply_document(
                document=out_file, caption=f'<code>{cmd}</code>', parse_mode=enums.ParseMode.HTML)
    else:
        await reply_to_.reply_text(final_output, parse_mode=enums.ParseMode.HTML)

    await message.delete()


@bot.on_message(filters.command("sh"))
async def sh(_, message):
    if message.from_user.id != OWNER_ID:
        return  # Ignore if not owner

    await message.reply("ᴀɴᴀʟʏᴢɪɴɢ ᴄᴏᴅᴇ...")

    reply_to_ = message.reply_to_message or message

    try:
        code = message.text.split(message.text.split()[0])[1]
    except:
        return await message.edit("ᴄᴀɴ ʏᴏᴜ ɪɴᴘᴜᴛ ᴛʜᴇ ᴄᴏᴅᴇ ᴛᴏ ʀᴜɴ ᴍʏ ᴘʀᴏɢʀᴀᴍ?")

    x = run(code)

    try:
        await reply_to_.reply_text(f"**ᴄᴏᴅᴇ**: ```{code}```\n\n**ʀᴇsᴜʟᴛs**:\n```{x}```")
    except MessageTooLong:
        with io.BytesIO(str.encode(x)) as logs:
            logs.name = "shell.txt"
            await reply_to_.reply_document(document=logs)

    await message.delete()
