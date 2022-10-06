print("Importing Modules...")
from disnake import Message, Activity, ActivityType
from pyfiglet import Figlet
from os import environ

f = Figlet(font="alligator")
from colorama import Fore

# import dbl as dblpy
import sys
from datetime import datetime
from logging import getLogger, INFO, StreamHandler, Formatter
from asyncio import sleep

from bot import Atomic

print("Initializing Logger...")
logger = getLogger("discord")
logger.setLevel(INFO)
handler = StreamHandler(sys.stdout)
handler.setFormatter(Formatter(f"%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
handler.setFormatter(Formatter(f"[{str(datetime.now())[:-10]}] %(name)s: %(message)s"))
logger.addHandler(handler)

client = Atomic(
    token=environ["TOKEN"],
    description="A general purpose Discord bot made by a middle schooler.",
    case_insensitive=True,
)


print(Fore.BLUE + f"{f.renderText('atomic')}")


@client.event
async def on_ready():
    print(Fore.BLUE + f"> signed in as {client.user.name} [{client.user.id}]")
    print(Fore.BLUE + f"> can see {len(client.guilds)} servers")
    print(
        Fore.BLUE
        + f"> loaded {len(client.slash_commands)} commands in {len(client.cogs)} cogs"
    )

    settings = client.db["settings"]
    for g in client.guilds:
        if await settings.count_documents({"_id": g.id}) == 0:
            await settings.insert_one(
                {
                    "_id": g.id,
                    "leveling": False,
                    "logging": False,
                    "welcoming": False,
                    "autorole": False,
                }
            )

    print(Fore.WHITE + f"[{str(datetime.now())[:-10]}] db is good")


@client.event
async def on_message(message: Message):
    if message.author.bot:
        return
    if message.content == "reload":
        c = [i for i in client.cogs]
        for i in c:
            client.reload_extension(f"cogs.{i}")
        await message.add_reaction("✅")
        return
    elif message.content == "load":
        c = [i for i in message.content.split(" ")[1:]]
        for i in c:
            try:
                client.load_extension(f"cogs.{i}")
            except Exception as e:
                print(e)
        await message.add_reaction("✅")
        return
    await client.process_commands(message)


# client.load_extension("jishaku")
# client.load_extension("cogs.Moderation")
# client.load_extension("cogs.Bot_Owner")
# client.load_extension("cogs.Welcome")
# client.load_extension("cogs.Help")
# client.load_extension("cogs.Economy")
client.load_extension("cogs.Fun")
# client.load_extension("cogs.stat")
# client.load_extension("cogs.Utility")
# client.load_extension("cogs.Music")
# client.load_extension("cogs.Config")
# client.load_extension("cogs.Level")
client.load_extension("cogs.Error")
client.load_extension("cogs.Bot_Info")


client.run()
