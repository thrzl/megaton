from disnake import Embed as _Embed
from disnake.ext.commands.context import Context
from datetime import datetime


class CategoryEmbed(_Embed):
    def __init__(self, ctx: Context, **kwargs):
        super().__init__(color=0x2F3136, **kwargs)
        if not kwargs["title"]:
            self.set_author(
                name=f"megaton {ctx.command.cog_name.upper()}",
                icon_url=ctx.bot.avatar_url,
            )


class Embed(_Embed):
    def __init__(self, **kwargs):
        super().__init__(color=0x2F3136, **kwargs)
