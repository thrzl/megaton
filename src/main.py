from disnake import Message
from dotenv import load_dotenv
load_dotenv()

from os import environ

import sys
from logging import getLogger, INFO, StreamHandler, Formatter

from bot import Megaton
from utils.check_env import check_env

logger = getLogger("discord")
logger.setLevel(INFO)
handler = StreamHandler(sys.stdout)
handler.setFormatter(Formatter(f"%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
# handler.setFormatter(Formatter(f"[{str(datetime.now())[:-10]}] %(name)s: %(message)s"))
logger.addHandler(handler)

check_env()

client = Megaton(
    token=environ["TOKEN"],
)


@client.event
async def on_ready():
    print(f"| signed in as {client.user.name} [{client.user.id}]")
    print(f"| can see {len(client.guilds)} servers")
    print(f"| loaded {len(client.slash_commands)} commands in {len(client.cogs)} cogs")


@client.event
async def on_message(message: Message):
    if message.author.bot or message.author.id not in client.owner_ids:
        return
    if message.content.startswith(client.user.mention):
        if "reload" in message.content:
            c = [i for i in client.cogs]
            for i in c:
                client.reload_extension(f"cogs.{i}")
            await message.add_reaction("✅")
        elif message.content.startswith("load"):
            c = [i for i in message.content.split(" ")[1:]]
            for i in c:
                try:
                    client.load_extension(f"cogs.{i}")
                except Exception as e:
                    print(e)
            await message.add_reaction("✅")
    return


# client.load_extension("jishaku")
client.load_extension("cogs.Moderation")
client.load_extension("cogs.Bot_Owner")
# client.load_extension("cogs.Welcome")
# client.load_extension("cogs.Help")
client.load_extension("cogs.Economy")
client.load_extension("cogs.Fun")
# client.load_extension("cogs.stat")
client.load_extension("cogs.Utility")
# client.load_extension("cogs.Music")
# client.load_extension("cogs.Config")
# client.load_extension("cogs.Level")
client.load_extension("cogs.Error")
client.load_extension("cogs.Bot_Info")


client.run()
