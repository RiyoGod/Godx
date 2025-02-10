from pyrogram import filters, enums
from pyrogram.types import Message
from Devine import devine
from requests import get
import datetime
import config
from Devine.helpers.help_func import make_carbon
import os
import asyncio
import requests
import httpx

timeout = httpx.Timeout(40, pool=None)
http = httpx.AsyncClient(http2=True, timeout=timeout)
weather_apikey = "8de2d8b3a93542c9a2d8b3a935a2c909"
get_coords = "https://api.weather.com/v3/location/search"
url = "https://api.weather.com/v3/aggcommon/v3-wx-observations-current"
headers = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; M2012K11AG Build/SQ1D.211205.017)"
}

@devine.on_message(filters.command("weather", prefixes=config.HANDLER) & filters.me)
async def weather(_, m: Message):
    if len(m.command) == 1:
        return await m.reply_text(
            "<b>ᴜsᴀɢᴇ:</b> <code>/weather location ᴏʀ city</code> - ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜᴇ ᴡᴇᴀᴛʜᴇʀ ɪɴ <i>ʟᴏᴄᴀᴛɪᴏɴ ᴏʀ ᴄɪᴛʏ</i>"
        )
    msg = await m.reply_text("ɢᴇᴛᴛɪɴɢ ᴡᴇᴀᴛʜᴇʀ ɪɴғᴏ...")

    r = await http.get(
        get_coords,
        headers=headers,
        params=dict(
            apiKey=weather_apikey,
            format="json",
            language="en",
            query=m.text.split(maxsplit=1)[1],
        ),
    )
    loc_json = r.json()
    try:
        await m.delete()
    except:
        return

    if not loc_json.get("location"):
        await msg.edit("ʟᴏᴄᴀᴛɪᴏɴ ɴᴏᴛ ғᴏᴜɴᴅ")
    else:
        pos = f"{loc_json['location']['latitude'][0]},{loc_json['location']['longitude'][0]}"
        r = await http.get(
            url,
            headers=headers,
            params=dict(
                apiKey=weather_apikey,
                format="json",
                language="en",
                geocode=pos,
                units="m",
            ),
        )
        res_json = r.json()

        obs_dict = res_json["v3-wx-observations-current"]

        res = "<b>{location}</b>:\n\nᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ: <code>{temperature} °C</code>\nᴛᴇᴍᴘᴇʀᴀᴛᴜʀᴇ ғᴇᴇʟs ʟɪᴋᴇ: <code>{feels_like} °C</code>\nᴀɪʀ ʜᴜᴍɪᴅɪᴛʏ: <code>{air_humidity}%</code>\nᴡɪɴᴅ sᴘᴇᴇᴅ: <code>{wind_speed} km/h</code>\n\n- <i>{overview}</i>".format(
            location=loc_json["location"]["address"][0],
            temperature=obs_dict["temperature"],
            feels_like=obs_dict["temperatureFeelsLike"],
            air_humidity=obs_dict["relativeHumidity"],
            wind_speed=obs_dict["windSpeed"],
            overview=obs_dict["wxPhraseLong"],
        )

        await msg.edit(res)

@devine.on_message(filters.command("carbon", prefixes=config.HANDLER) & filters.me)
async def carbon(_, m: Message):
    msg = await m.reply_text("Trying...")
    if m.reply_to_message:
        if m.reply_to_message.text:
            txt = m.reply_to_message.text
        else:
            return await msg.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    else:
        try:
            txt = m.text.split(None, 1)[1]
        except IndexError:
            return await msg.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ.")
    m = await msg.edit("ɢᴇɴᴇʀᴀᴛɪɴɢ ᴄᴀʀʙᴏɴ...")
    carbon = await make_carbon(txt)
    await m.edit("ᴜᴩʟᴏᴀᴅɪɴɢ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ...")
    await devine.send_photo(m.chat.id, photo=carbon)
    await m.delete()
    carbon.close()

async def convert_to_datetime(timestamp):
    try:
        date = datetime.datetime.fromtimestamp(timestamp)
        return date
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return ""

async def spacebin(text: str):
    url = "https://spaceb.in/api/v1/documents/"
    response = requests.post(url, data={"content": text, "extension": "txt"})
    id = response.json().get('payload').get('id')
    res = requests.get(f"https://spaceb.in/api/v1/documents/{id}").json()
    created_at = res.get("payload").get("created_at")
    link = f"https://spaceb.in/{id}"
    raw = f"https://spaceb.in/api/v1/documents/{id}/raw"
    timedate = await convert_to_datetime(created_at)
    string = f"""\u0020
**Here's the link**: **[Paste link]({link})**
**Here's the link**: **[Raw View]({raw})**
**Created datetime**: {timedate}
"""
    return string
