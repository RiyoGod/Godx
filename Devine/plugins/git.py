from pyrogram import filters
from Devine import devine
from requests import get
import os
import config


@devine.on_message(filters.me & filters.command("git", prefixes=config.HANDLER))
async def git(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**ᴡʜᴇʀᴇ ʏᴏᴜ ɪɴᴘᴜᴛ ᴛʜᴇ ᴜsᴇʀɴᴀᴍᴇ?**")
    
    user = message.text.split(None, 1)[1]
    res = get(f"https://api.github.com/users/{user}").json()

    if "message" in res and res["message"] == "Not Found":
        return await message.reply_text("**ɴᴏ ɢɪᴛʜᴜʙ ᴜsᴇʀ ᴡɪᴛʜ ᴛʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ!**")

    name = res.get("name", "ᴜɴᴋɴᴏᴡɴ")
    bio = res.get("bio", "ɴᴏ ʙɪᴏ")
    company = res.get("company", "ɴᴏ ᴄᴏᴍᴘᴀɴʏ")
    blog = res.get("blog", "ɴᴏ ʙʟᴏɢ")
    location = res.get("location", "ɴᴏ ʟᴏᴄᴀᴛɪᴏɴ")
    public_repos = res.get("public_repos", "𝟶")
    followers = res.get("followers", "𝟶")
    following = res.get("following", "𝟶")
    created_at = res.get("created_at", "ᴜɴᴋɴᴏᴡɴ")

    data = f"""**ɴᴀᴍᴇ**: {name}
**ᴜsᴇʀɴᴀᴍᴇ**: `{res['login']}`
**ʟɪɴᴋ**: [{res['login']}]({res['html_url']})
**ʙɪᴏ**: {bio}
**ᴄᴏᴍᴘᴀɴʏ**: {company}
**ʙʟᴏɢ**: {blog}
**ʟᴏᴄᴀᴛɪᴏɴ**: {location}
**ᴘᴜʙʟɪᴄ ʀᴇᴘᴏs**: `{public_repos}`
**ꜰᴏʟʟᴏᴡᴇʀs**: `{followers}`
**ꜰᴏʟʟᴏᴡɪɴɢ**: `{following}`
**ᴀᴄᴄ ᴄʀᴇᴀᴛᴇᴅ**: `{created_at}`
"""

    try:
        file_path = f"{user}.jpg"
        with open(file_path, "wb") as f:
            f.write(get(res["avatar_url"]).content)
        
        await message.reply_photo(file_path, caption=data)
        os.remove(file_path)
    except Exception as e:
        return await message.reply_text(f"**ᴇʀʀᴏʀ:** `{e}`")

    await message.delete()
