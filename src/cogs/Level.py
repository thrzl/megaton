from disnake.ext import commands
from src.bot import Megaton
from disnake import Message, GuildCommandInteraction, Member


class Level(commands.Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
        if not bot.db:
            raise ValueError("database connection not yet initialized")
        self.db = bot.db
        self.enabled_guilds: set[int] = set()

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author == self.bot.user or message.author.bot or not message.guild:
            return

        author = message.author.id

        level_data = await self.db.get_level_data(author, message.guild.id)
        if not level_data:
            return
        old_level = level_data.level
        await level_data.update_xp(1)
        new_level = level_data.level
        if new_level > old_level:
            embed = (
                self.bot.Embed(
                    description=f"congrats <@{author}>, you've reached level {new_level}!"
                )
                .set_author(
                    name=message.author.display_name,
                    icon_url=message.author.display_avatar.url,
                )
                .set_footer(
                    text="congrats! you leveled up! keep chatting to level up more!"
                )
            )
            await message.channel.send(embed=embed)

    @commands.slash_command(
        name="level",
        description="check your level and xp in this guild",
        aliases=["xp"],
    )
    @commands.guild_only()
    async def xp(
        self, ctx: GuildCommandInteraction[Megaton], who: Member | None = None
    ):
        if not ctx.guild:
            return
        member = who or ctx.author
        level_data = await self.db.get_level_data(member.id, ctx.guild.id)
        if level_data:
            embed = self.bot.Embed(
                description=f"XP: **{level_data.xp}**\nlevel: **{level_data.level}**",
            ).set_author(
                name=f"{member.name}'s level in {ctx.guild.name}",
                icon_url=member.display_avatar.url,
            )
        else:
            embed = self.bot.Embed(
                description="leveling isn't enabled in this guild.",
            ).set_author(
                name=f"{member.name}'s level in {ctx.guild.name}",
                icon_url=member.display_avatar.url,
            )
        await ctx.send(embed=embed)


def setup(bot: Megaton):
    bot.add_cog(Level(bot))
