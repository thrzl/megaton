from typing import Optional
from disnake import Intents, Member, Embed as _Embed, Activity, ActivityType
from disnake.types.embed import Embed as EmbedData
from disnake.ext.commands.bot import InteractionBot
from datetime import datetime, timedelta
from enum import Enum
from os import environ
from asyncio import sleep
from statcord import StatcordClient


class FalseVaccum(Exception):
    pass


class HeirarchyError(Exception):
    text: Optional[str] = None


class HeirarchyErrorType(Enum):
    NO_PERMISSION = 0
    SELF_NO_PERMISSION = 1


class Embed(_Embed):
    __slots__ = (
        "title",
        "url",
        "type",
        "_timestamp",
        "_colour",
        "_footer",
        "_image",
        "_thumbnail",
        "_video",
        "_provider",
        "_author",
        "_fields",
        "description",
        "_files",
        "preserve_case",
    )

    def __init__(self, color=0x2F3136, preserve_case=False, **kwargs):
        super().__init__(color=color, **kwargs)
        self.preserve_case = preserve_case

    def to_dict(self) -> EmbedData:
        if not self.preserve_case:
            f = self.fields
            self.clear_fields()
            for field in f:
                self.add_field(
                    name=field.name.lower() if field.name else None,
                    value=field.value.lower() if field.value else None,
                    inline=field.inline if field.inline is not None else True,
                )
            if self._footer:
                self._footer["text"] = self._footer["text"].lower()
                self.set_footer(**{k: v for k, v in self._footer.items()})  # type: ignore
            if self._author:
                self.set_author(**{k: v for k, v in self._author.items()})  # type: ignore
            if self.title:
                self.title = self.title.lower()
            if self.description:
                self.description = self.description.lower()
        return super().to_dict()


class Megaton(InteractionBot):

    def __init__(self, token: str, intents: Intents = None, *args, **kwargs):
        super().__init__()
        if not intents:
            intents = Intents.all()
            intents.message_content = True
        self.token = token
        self.Embed = Embed
        self.loop.create_task(self.ch_pr())
        self.statcord_client = StatcordClient(self, environ["STATCORD_KEY"])
        # dbl = dblpy.DBLClient(
        #     client,
        #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NjgxODkxMTUwNTA4ODUxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MzI0Mjc5fQ.ADjcN7pcHL9D5lfnGYHPQH8lXQyvqxzcWg7jSHLIgrs",
        #     True,
        #     webhook_auth="tPL8UP3qyn9XikHOA9357QpGEEawK2bv",
        #     webhook_path="/dblhookmegaton",
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
        while not self.is_closed():
            mc = sum(guild.member_count for guild in self.guilds)
            await self.change_presence(
                activity=Activity(
                    name=f"{mc} members in {len(self.guilds)} guilds",
                    type=ActivityType.listening,
                )
            )
            await sleep(120)

    def load_extension(self, name: str):
        super().load_extension(name)
        n = name.split(".")[-1].replace("_", " ")
        print(f"| loaded {n.lower()} features")
