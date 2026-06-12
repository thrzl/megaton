from disnake import Member
from disnake.ext import commands
import disnake
from colorthief import ColorThief
from io import BytesIO
from src.bot import Embed, Megaton


async def get_color(img: BytesIO) -> tuple[int, int, int]:
    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)
    return dominant_color


class Welcome(commands.Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
        if not bot.db:
            raise Exception("database connection is not established.")
        self.db = bot.db

    async def member_exit_handler(self, member: Member):
        welcome_config = await self.db.get_guild_settings(member.guild.id)
        welcome_channel_id = welcome_config.welcoming

        if welcome_channel_id == 0:
            return

        welcome_channel = await self.bot.fetch_channel(welcome_channel_id)
        # eg = await self.bot.fetch_guild(member.guild.id)

        image_bytes = BytesIO(await member.display_avatar.read())
        red, green, blue = await get_color(image_bytes)
        embed = Embed(
            title=f"goodbye {member.name}",
            description=f"thanks for visiting {member.guild.name}!",
            color=disnake.Color.from_rgb(red, green, blue).value,
        ).set_thumbnail(url=member.display_avatar.url)
        await welcome_channel.send(embed=embed)  # ty:ignore[unresolved-attribute]

    @commands.Cog.listener()
    async def on_member_leave(self, member: Member):
        await self.member_exit_handler(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member: Member):
        return await self.member_exit_handler(member)

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        welcome_config = await self.db.get_guild_settings(member.guild.id)
        welcome_channel_id = welcome_config.welcoming

        if welcome_channel_id == 0:
            return

        welcome_channel = await self.bot.fetch_channel(welcome_channel_id)

        image_bytes = BytesIO(await member.display_avatar.read())
        red, green, blue = await get_color(image_bytes)
        embed = Embed(
            title=f"welcome {member.name} 🎉",
            description=f"welcome to {member.guild.name}! we hope you have a great time here!",
            color=disnake.Color.from_rgb(red, green, blue).value,
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await welcome_channel.send(embed=embed)


def setup(bot: Megaton):
    bot.add_cog(Welcome(bot))
