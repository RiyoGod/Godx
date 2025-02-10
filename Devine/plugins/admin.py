import config
from pyrogram import filters, enums
from pyrogram.types import ChatPrivileges
from Devine import devine, MODULE


@devine.on_message(filters.command(["promote", "fpromote"], prefixes=config.HANDLER) & filters.me)
async def promote_member(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.command[1])
        except (IndexError, ValueError):
            return await message.edit("**ɪɴᴘᴜᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ!**")

    try:
        my_privileges = (await message.chat.get_member(user_id=message.from_user.id)).privileges
        if not my_privileges or not my_privileges.can_promote_members:
            return await message.edit("**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ `ᴄᴀɴ_ᴘʀᴏᴍᴏᴛᴇ_ᴍᴇᴍʙᴇʀs` ʀɪɢʜᴛs!**")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")

    command = message.command[0]
    if command == "fpromote":
        await message.chat.promote_member(user_id=user_id, privileges=my_privileges)
        return await message.edit("**ꜰᴜʟʟʏ ᴘʀᴏᴍᴏᴛᴇᴅ!**")
    else:
        privileges = ChatPrivileges(
            can_delete_messages=True, can_restrict_members=True,
            can_change_info=True, can_invite_users=True, can_pin_messages=True,
            can_manage_video_chats=True
        )
        await message.chat.promote_member(user_id=user_id, privileges=privileges)
        return await message.edit("**ᴘʀᴏᴍᴏᴛᴇᴅ!**")


@devine.on_message(filters.command(["pin", "unpin"], prefixes=config.HANDLER) & filters.me)
async def messages_pin(_, message):
    if not message.reply_to_message:
        return await message.edit("**ɴᴏ ʀᴇᴘʟʏ?**")

    command = message.command[0]
    link = message.reply_to_message.link

    try:
        if command == "pin":
            await message.reply_to_message.pin()
            return await message.edit(f"**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ [ᴘɪɴɴᴇᴅ]({link})!**")
        else:
            await message.reply_to_message.unpin()
            return await message.edit(f"**ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ [ᴜɴᴘɪɴɴᴇᴅ]({link})!**")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@devine.on_message(filters.command("invite", prefixes=config.HANDLER) & filters.me)
async def invite_link(_, message):
    try:
        link = (await devine.get_chat(message.chat.id)).invite_link
        return await message.edit(f"**ɪɴᴠɪᴛᴇ ʟɪɴᴋ:** `{link}`")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@devine.on_message(filters.command("admins", prefixes=config.HANDLER) & filters.me)
async def admins_list(_, message):
    chat_id = message.chat.id
    msg = await message.edit("**ᴀɴᴀʟʏᴢɪɴɢ ᴀᴅᴍɪɴs...**")
    text = f"**ᴀᴅᴍɪɴs ɪɴ {message.chat.title}:**\n"

    try:
        async for admin in devine.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.user.is_bot:
                text += f"• [{admin.user.first_name}](tg://user?id={admin.user.id})\n"
    except Exception as e:
        return await msg.edit(f"**ᴇʀʀᴏʀ:** `{e}`")

    return await msg.edit(text)


@devine.on_message(filters.command("del", prefixes=config.HANDLER) & filters.me)
async def delete_message(_, message):
    if message.reply_to_message:
        try:
            await message.reply_to_message.delete()
            return await message.delete()
        except Exception as e:
            return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")
    else:
        return await message.edit("**ɴᴏ ʀᴇᴘʟʏ?**")


@devine.on_message(filters.command("ban", prefixes=config.HANDLER) & filters.me)
async def ban_member(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.command[1])
        except (IndexError, ValueError):
            return await message.edit("**ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ_ɪᴅ ᴛᴏ ʙᴀɴ!**")

    try:
        await message.chat.ban_member(user_id)
        name = (await devine.get_users(user_id)).first_name
        return await message.edit(f"**{name} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ!**")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@devine.on_message(filters.command("unban", prefixes=config.HANDLER) & filters.me)
async def unban_member(_, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        try:
            user_id = int(message.command[1])
        except (IndexError, ValueError):
            return await message.edit("**ᴘʀᴏᴠɪᴅᴇ ᴜsᴇʀ_ɪᴅ ᴛᴏ ᴜɴʙᴀɴ!**")

    try:
        await message.chat.unban_member(user_id)
        name = (await devine.get_users(user_id)).first_name
        return await message.edit(f"**{name} ʜᴀs ʙᴇᴇɴ ᴜɴʙᴀɴɴᴇᴅ!**")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")


@devine.on_message(filters.command("purge", prefixes=config.HANDLER) & filters.me)
async def purge(_, message):
    if not message.reply_to_message:
        return await message.edit("**ɴᴏ ʀᴇᴘʟʏ?**")

    chat_id = message.chat.id
    reply_msg_id = message.reply_to_message.id
    message_id = message.id
    message_ids = list(range(reply_msg_id, message_id))

    try:
        await devine.delete_messages(chat_id=chat_id, message_ids=message_ids)
        return await message.edit(f"**ᴘᴜʀɢᴇᴅ {len(message_ids)} ᴍᴇssᴀɢᴇs**")
    except Exception as e:
        return await message.edit(f"**ᴇʀʀᴏʀ:** `{e}`")
