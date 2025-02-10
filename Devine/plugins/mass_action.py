from pyrogram import filters, enums
from pyrogram.types import *
from Devine import devine as bot
from config import HANDLER, OWNER_ID


async def is_owner(chat_id: int, user_id: int):
    """Check if the user is the chat owner."""
    async for member in bot.get_chat_members(chat_id):
        if member.status == enums.ChatMemberStatus.OWNER and member.user.id == user_id:
            return True
    return False


async def is_admin(chat_id: int, user_id: int):
    """Check if the user is an admin in the chat."""
    async for admin in bot.get_chat_administrators(chat_id):
        if admin.user.id == user_id:
            return True
    return False


def is_owner_or_admin(user_id: int, chat_id: int):
    """Check if user is in OWNER_ID or an admin in chat."""
    if isinstance(OWNER_ID, int) and user_id == OWNER_ID:
        return True
    if isinstance(OWNER_ID, list) and user_id in OWNER_ID:
        return True
    return is_owner(chat_id, user_id)


@bot.on_message(filters.command(["unbanall", "massunban"], prefixes=HANDLER))
async def unbanall(_, message):
    """Unban all users in a chat."""
    user_id, chat_id = message.from_user.id, message.chat.id

    if not await is_owner_or_admin(user_id, chat_id):
        return await message.reply("**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴄᴄᴇss ᴛʜɪs!**")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        banned_users = [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED)]

        if not banned_users:
            return await message.reply("**ɴᴏ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ᴛᴏ ᴜɴʙᴀɴ!**")

        for user in banned_users:
            await bot.unban_chat_member(chat_id, user)

        await message.reply(f"**ᴜɴʙᴀɴɴᴇᴅ** `{len(banned_users)}` **ᴜsᴇʀs sᴜᴄᴄᴇssғᴜʟʟʏ!**")
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")


@bot.on_message(filters.command(["sbanall", "banall", "massban"], prefixes=HANDLER))
async def banall(_, message):
    """Ban all non-admin members in a chat."""
    user_id, chat_id = message.from_user.id, message.chat.id

    if not await is_owner_or_admin(user_id, chat_id):
        return await message.reply("**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴄᴄᴇss ᴛʜɪs!**")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        members = [member.user.id async for member in bot.get_chat_members(chat_id) if not await is_admin(chat_id, member.user.id)]

        if not members:
            return await message.reply("**ɴᴏ ᴍᴇᴍʙᴇʀs ᴛᴏ ʙᴀɴ!**")

        for member in members:
            await bot.ban_chat_member(chat_id, member)

        await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ʙᴀɴɴᴇᴅ** `{len(members)}` **ᴜsᴇʀs!**")
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")


@bot.on_message(filters.command(["skickall", "kickall", "masskick"], prefixes=HANDLER))
async def kickall(_, message):
    """Kick all non-admin members in a chat."""
    user_id, chat_id = message.from_user.id, message.chat.id

    if not await is_owner_or_admin(user_id, chat_id):
        return await message.reply("**ʏᴏᴜ ᴄᴀɴ'ᴛ ᴀᴄᴄᴇss ᴛʜɪs!**")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs!**")

    try:
        members = [member.user.id async for member in bot.get_chat_members(chat_id) if not await is_admin(chat_id, member.user.id)]

        if not members:
            return await message.reply("**ɴᴏ ᴍᴇᴍʙᴇʀs ᴛᴏ ᴋɪᴄᴋ!**")

        for member in members:
            await bot.ban_chat_member(chat_id, member)
            await bot.unban_chat_member(chat_id, member)

        await message.reply(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ** `{len(members)}` **ᴜsᴇʀs!**")
    except Exception as e:
        await message.reply(f"**ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ:** `{e}`")
