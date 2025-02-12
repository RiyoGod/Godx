import os
import time
import logging
from pyrogram import Client
from pymongo import MongoClient
import motor.motor_asyncio

FORMAT = "[Devine]: %(message)s"

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('logs.txt'),
                                                    logging.StreamHandler()], format=FORMAT)
StartTime = time.time()

MODULE = []

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


logger = logging.getLogger(__name__)

DB_URL = os.getenv("DB_URL", "mongodb+srv://jc07cv9k3k:bEWsTrbPgMpSQe2z@cluster0.nfbxb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
API_ID = int(os.getenv("API_ID", 26416419))
API_HASH = os.getenv("API_HASH", "c109c77f5823c847b1aeb7fbd4990cc4")
SESSION = os.getenv("SESSION", "BQGTFSMAGFSHoO6fzim5zwSjuJcxbG21Nmlvatg3cDPmGFnFPeMh5d7Kn1wlc1Hbb2V4BXWecDBVy2KnkBYbJ4A_p9_qbx1e8ajByK7Oy8uw8GRnQo_6TTz3MP1MeTeZ0z6sGiIw2IU2e_xC_w7sCN5tRLC8-3uFuDbS2_J5rU0UBVyJq9293FfKAOW8WsnaU30ZEr9sxcc1GOlplF6x8NRla_svibYnOFXXIt-sbrc1QpxJR5puoYefgnVnPa3v3Uvbb2Yv1eEfo0OfFTwhL0Zijjm69320RfEIy34GjeolAxNfdUG6abYrm6V_8oMTpPo8T7xAnP2nOw5UNNiUjRCflvB55QAAAAHJtXFRAA")
TOKEN = os.getenv("TOKEN", "7636486844:AAFs25A-FAXvjNSAro_LthgB8GamrlZ_5n4")
DB_NAME = os.getenv("DB_NAME", "None")

cli = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db=cli[DB_NAME]

DB = MongoClient(DB_URL)
DATABASE = DB[DB_NAME]

devine = Client(name="Devine", session_string=SESSION, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Devine"))
bot = Client(name="Devine", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=dict(root="Devine"))


class INFO:
   def devine():
      info = devine.get_me()
      return info   
     
   def bot():
      info = bot.get_me()
      return info
   
