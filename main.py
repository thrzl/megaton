from os import environ

from disnake import Message
from dotenv import load_dotenv

from src.bot import Megaton
from src.db import Database
from src.utils.check_env import check_env
from src.utils.log import log

load_dotenv()
check_env()

test_guilds = (
    [int(guild) for guild in environ["TEST_GUILDS"].split(",")]
    if environ.get("TEST_GUILDS")
    else []
)
owner_ids = (
    [int(owner) for owner in environ["OWNER_IDS"].split(",")]
    if environ.get("OWNER_IDS")
    else []
)
client = Megaton(
    token=environ["TOKEN"],
    test_guilds=test_guilds,
    owner_ids=owner_ids,
)


@client.event
async def on_ready():
    client.db = await Database.create(environ["DB_PATH"])

    client.load_extension("src.cogs.Config")
    client.load_extension("src.cogs.Welcome")
    log.info(f"signed in as {client.user.name} [{client.user.id}]")
    log.info(f"can see {len(client.guilds)} servers")
    log.info(f"loaded {len(client.slash_commands)} commands in {len(client.cogs)} cogs")
    log.info(f"test guilds: {client._test_guilds or '(none)'}")
    log.info(f"owner ids: {client.owner_ids or '(none)'}")


@client.event
async def on_message(message: Message):
    if message.author.bot or message.author.id not in client.owner_ids:
        return
    if message.content.startswith(client.user.mention):
        if "reload" in message.content:
            c = [i for i in client.cogs]
            for i in c:
                client.reload_extension(f"src.cogs.{i}")
            await message.add_reaction("✅")
        elif message.content.startswith("load"):
            c = [i for i in message.content.split(" ")[1:]]
            for i in c:
                try:
                    client.load_extension(f"src.cogs.{i}")
                except Exception as e:
                    log.error(f"failed to load extension: {e}")
            await message.add_reaction("✅")
    return


# client.load_extension("src.cogs.Moderation")
client.load_extension("src.cogs.Bot_Owner")
# client.load_extension("src.cogs.Help")
# client.load_extension("src.cogs.Economy")
# client.load_extension("src.cogs.Fun")
client.load_extension("src.cogs.Utility")
# client.load_extension("src.cogs.Music")
# client.load_extension("src.cogs.Level")
client.load_extension("src.cogs.Error")
client.load_extension("src.cogs.Bot_Info")


client.run()
