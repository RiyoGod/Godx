import pyrogram
import strings
import config

from Devine import bot , devine
from Devine.helpers.help_func import get_datetime 

async def run_clients():
      await bot.start()
      await devine.start()
      await pyrogram.idle()
      zone = await get_datetime()
      await bot.send_message(
           chat_id=config.GROUP_ID,
           text=strings.RESTART_TEXT1.format(date=zone["date"], time=zone["time"]))
      await devine.send_message(
           chat_id=config.GROUP_ID,
           text=strings.RESTART_TEXT2.format(date=zone["date"], time=zone["time"]))


if __name__ == "__main__":
    devine.loop.run_until_complete(run_clients())
