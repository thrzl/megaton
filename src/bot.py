from disnake import Intents, Member, Embed, Activity, ActivityType
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.bot import when_mentioned_or
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
from enum import Enum
from os import environ
from asyncio import sleep


class FalseVaccum(Exception):
    pass


class HeirarchyError(Exception):
    pass


class HeirarchyErrorType(Enum):
    NO_PERMISSION = 0
    SELF_NO_PERMISSION = 1


class AEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(color=0x2F3136, **kwargs)
        self.timestamp = datetime.utcnow()


class Atomic(Bot):
    db: AsyncIOMotorClient

    def __init__(self, token: str, intents: Intents = None, *args, **kwargs):
        super().__init__(command_prefix=when_mentioned_or("a!"))
        if not intents:
            intents = Intents.all()
            intents.message_content = True
        self.token = token
        db = AsyncIOMotorClient(environ["DATABASE_URL"])
        self.db = db["atomic"]
        self.Embed = AEmbed
        self.loop.create_task(self.ch_pr())
        # dbl = dblpy.DBLClient(
        #     client,
        #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NjgxODkxMTUwNTA4ODUxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MzI0Mjc5fQ.ADjcN7pcHL9D5lfnGYHPQH8lXQyvqxzcWg7jSHLIgrs",
        #     True,
        #     webhook_auth="tPL8UP3qyn9XikHOA9357QpGEEawK2bv",
        #     webhook_path="/dblhookatomic",
        # )

    def run(self):
        super().run(self.token)

    def calculate_time(self, time: str):
        td = {"d": 86400, "h": 3600, "m": 60, "s": 1}
        try:
            seconds = td[time[-1]] * int(time[:-1])
        except KeyError:
            raise FalseVaccum("Please use a time such as 1d, 5m, or 2h")
        end = datetime.now() + timedelta(seconds=seconds)
        return seconds, end

    def check_heirarchy(self, user: Member, victim: Member):
        guild = victim.guild
        if (
            victim.top_role.position >= user.top_role.position
            and guild.owner_id != user.id
        ):
            return HeirarchyErrorType.NO_PERMISSION
        if victim.top_role.position >= guild.me.top_role.position:
            return HeirarchyErrorType.SELF_NO_PERMISSION

    async def ch_pr(self):
        await self.wait_until_ready()
        # statuses = ["that's really cool and all, but i don't remember asking","i looked through the fbi records, but i couldn't find a single person who asked","billy la bufanda's a player bro","when in doubt, mumble","no","nothing sucks more than that moment during an argument when you realize you’re wrong","myself","glade air freshener","when the virus is over, i still want to stay away from some of you","I hope life isn't a joke, because i don't get it","the purpose of life is a life of purpose","when life gives you lemons, throw them at people","with fork bombs on his main pc 👀","i'm nobody. nobody's perfect. therefore, i'm perfect","i wish i were you so i could be friends with me","some people just need a high-five to the face","Parachute for sale, used once, never opened!","a prank on you","a game","with love 💔","literally nothing","a prank on you","Yourself","RealLife.exe","unknown","as a bot","got kilig before thrzl lmao","Slideee by Zay Ade","with Auttaja","his teacher lol","Discord",f"on {len(self.guilds)} servers", "Among You","with Rapptz","Amidst Thee","i like ya cut g"]
        # statusnumber = len(statuses)
        # print(f"{str(statusnumber)} statuses.")
        while not self.is_closed():
            # status = random.choice(statuses)
            mc = 0
            guilds = self.guilds
            for i in guilds:
                mc += i.member_count
            await self.change_presence(
                activity=Activity(
                    name=f"{mc} members in {len(guilds)} guilds",
                    type=ActivityType.listening,
                )
            )
            await sleep(120)

    def load_extension(self, name: str):
        super().load_extension(name)
        print(f"Loaded {name}")
