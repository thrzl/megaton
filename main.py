import sys
from logging import INFO, Formatter, StreamHandler, getLogger
from os import environ

from disnake import Message
from dotenv import load_dotenv

from src.bot import Megaton
from src.utils.check_env import check_env

load_dotenv()

logger = getLogger("discord")
logger.setLevel(INFO)
handler = StreamHandler(sys.stdout)
handler.setFormatter(Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

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
# client.load_extension("src.cogs.Moderation")
client.load_extension("src.cogs.Bot_Owner")
# client.load_extension("src.cogs.Welcome")
# client.load_extension("src.cogs.Help")
# client.load_extension("src.cogs.Economy")
# client.load_extension("src.cogs.Fun")
client.load_extension("src.cogs.Utility")
# client.load_extension("src.cogs.Music")
# client.load_extension("src.cogs.Config")
# client.load_extension("src.cogs.Level")
client.load_extension("src.cogs.Error")
client.load_extension("src.cogs.Bot_Info")


client.run()
