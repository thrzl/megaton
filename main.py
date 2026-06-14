from os import environ

from disnake import Message
from dotenv import load_dotenv

from src.bot import Megaton
from src.db import Database
from src.utils.check_env import check_env
from src.utils.log import log

from asyncio import run as asyncio_run

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
        args = message.content.split(" ")[1:]
        if "reload" in message.content:
            c = [i for i in client.cogs]
            for i in c:
                client.reload_extension(f"src.cogs.{i}")
            await message.add_reaction("✅")
        elif args[0] == "load":
            for cog in args[1:]:
                try:
                    client.load_extension(f"src.cogs.{cog}")
                except Exception as e:
                    log.error(f"failed to load extension: {e}")
            await message.add_reaction("✅")
    return


async def main():
    client.db = await Database.create(environ["DB_PATH"])
    ENABLED_COGS = (
        "Config",
        "Welcome",
        # "Moderation",
        "Bot_Owner",
        # "Help",
        # "Economy",
        # "Fun",
        "Utility",
        # "Music",
        # "Level",
        "Error",
        "Bot_Info",
    )
    for cog in ENABLED_COGS:
        try:
            client.load_extension(f"src.cogs.{cog}")
        except Exception as e:
            log.error(f"failed to load extension: {e}")
    await client.start(client.token)


asyncio_run(main())
