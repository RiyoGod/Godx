from pyrogram import filters, enums
from pyrogram.types import Message
from asyncio import sleep
from Devine import devine as bot
from config import HANDLER, OWNER_ID


async def is_owner(chat_id: int, user_id: int) -> bool:
    """Check if the user is the chat owner."""
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status == enums.ChatMemberStatus.OWNER
    except Exception:
        return False


async def is_admin(chat_id: int, user_id: int) -> bool:
    """Check if the user is an admin."""
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status in {enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR}
    except Exception:
        return False


@bot.on_message(filters.me & filters.command(["unbanall", "massunban"], prefixes=HANDLER))
async def unbanall(_, message: Message):
    """Unban all banned users in a chat."""
    
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        banned_users = [
            member.user.id
            async for member in bot.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BANNED)
            if member.user
        ]

        if not banned_users:
            return await message.reply("**ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ᴛᴏ ᴜɴʙᴀɴ!**")

        for user in banned_users:
            await bot.unban_chat_member(message.chat.id, user)
            await sleep(0.5)  # Prevents flood wait

        await message.reply(f"**ᴜɴʙᴀɴɴᴇᴅ** `{len(banned_users)}` **ᴜsᴇʀs sᴜᴄᴄᴇssғᴜʟʟʏ!**")

    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")


@bot.on_message(filters.me & filters.command(["sbanall", "banall", "massban"], prefixes=HANDLER))
async def banall(_, message: Message):
    """Ban all non-admin members in a chat."""
    
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        members = [
            member.user.id
            async for member in bot.get_chat_members(message.chat.id)
            if not await is_admin(message.chat.id, member.user.id)
        ]

        if not members:
            return await message.reply("**ɴᴏ ᴍᴇᴍʙᴇʀs ᴛᴏ ʙᴀɴ!**")

        for member in members:
            await bot.ban_chat_member(message.chat.id, member)
            await sleep(0.5)  # Prevents flood wait

        await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ** `{len(members)}` **ᴜsᴇʀs!**")
    
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")


@bot.on_message(filters.me & filters.command(["skickall", "kickall", "masskick"], prefixes=HANDLER))
async def kickall(_, message: Message):
    """Kick all non-admin members in a chat."""
    
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        members = [
            member.user.id
            async for member in bot.get_chat_members(message.chat.id)
            if not await is_admin(message.chat.id, member.user.id)
        ]

        if not members:
            return await message.reply("**ɴᴏ ᴍᴇᴍʙᴇʀs ᴛᴏ ᴋɪᴄᴋ!**")

        for member in members:
            await bot.ban_chat_member(message.chat.id, member)
            await bot.unban_chat_member(message.chat.id, member)
            await sleep(0.5)  # Prevents flood wait

        await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ** `{len(members)}` **ᴜsᴇʀs!**")
    
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")
