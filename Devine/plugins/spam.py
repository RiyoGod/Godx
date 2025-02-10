import asyncio
from pyrogram.types import Message
from pyrogram import filters
from Devine import devine, MODULE
import config

@devine.on_message(filters.command(["shelp"], prefixes=config.HANDLER) & filters.me)
async def delay_handler(_, m: Message):
    try:
        reply = m.reply_to_message
        cmd = m.command

        if len(m.command) < 3:
            await devine.send_message(m.chat.id, f"ᴜsᴇ ʟɪᴋᴇ ᴛʜɪs: `{config.HANDLER}dspam [ᴄᴏᴜɴᴛ sᴘᴀᴍ] [ᴅᴇʟᴀʏ ᴛɪᴍᴇ ɪɴ sᴇᴄᴏɴᴅs] [ᴛᴇxᴛ ᴍᴇssᴀɢᴇs]`")

        elif len(m.command) > 2 and not reply:
            await m.delete()
            msg = m.text.split(None, 3)
            times = int(msg[1]) if msg[1].isdigit() else None
            sec = int(msg[2]) if msg[2].isdigit() else None
            text = msg[3]
            for x in range(times):
                await devine.send_message(m.chat.id, text)
                await asyncio.sleep(sec)
        else:
            await devine.send_message(m.chat.id, "sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ɪɴ sᴘᴀᴍ ᴄᴏᴍᴍᴀɴᴅ !")
    except Exception as e:
        print(e)

@devine.on_message(filters.command(["spam"], prefixes=config.HANDLER) & filters.me)
async def spam_handler(_, m: Message):
    try:
        reply = m.reply_to_message
        reply_to_id = reply.message_id if reply else None
        cmd = m.command

        if not reply and len(cmd) < 2:
            await devine.send_message(m.chat.id, f"ᴜsᴇ ʟɪᴋᴇ ᴛʜɪs: {config.HANDLER}spam [ᴄᴏᴜɴᴛ sᴘᴀᴍ] [ᴛᴇxᴛ ᴍᴇssᴀɢᴇs]")
            return

        if not reply and len(cmd) > 1:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else None
            text = " ".join(cmd[2:]).strip()
            if not text:
                await devine.send_message(m.chat.id, "ᴛʜᴇ sᴘᴀᴍ ᴛᴇxᴛ ᴄᴀɴɴᴏᴛ ʙᴇ ᴇᴍᴘᴛʏ.")
                return

            for x in range(times):
                await devine.send_message(m.chat.id, text)
                await asyncio.sleep(0.10)

        elif reply:
            await m.delete()
            times = int(cmd[1]) if cmd[1].isdigit() else None
            for x in range(times):
                await devine.copy_message(m.chat.id, m.chat.id, reply.message_id)
    except Exception as e:
        print(e)

@devine.on_message(filters.command(["cspam"], prefixes=config.HANDLER) & filters.me)
async def send_msg(_, m: Message):
    id = int(m.command[1])
    cmd = m.command
    text = " ".join(cmd[2:]).strip()

    if len(cmd) < 2:
        await m.reply_text(f"ᴜsᴇ ʟɪᴋᴇ ᴛʜɪs: {config.HANDLER}smsg [ᴜsᴇʀ/ᴄʜᴀᴛɪᴅ] [ᴛᴇxᴛ ᴍᴇssᴀɢᴇs]")
        return
    msg = await m.reply_text("ᴛʀʏɪɴɢ ᴛᴏ sᴇɴᴅ ᴍsɢ...")

    try:
        await devine.send_message(id, text)
        await msg.edit("sᴇɴᴛ sᴜᴄᴄᴇssғᴜʟʟʏ")
    except Exception as err:
        await msg.edit(f"ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!\n{err}")
    
    try:
        await m.delete()
    except:
        return
