from disnake.ext.commands.cog import Cog
from disnake.ext.commands.slash_core import slash_command
import disnake
import sys

from bot import Megaton, Embed


class Bot_Info(Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot

    @slash_command(
        name="vote",
        description="Vote for megaton and get your voter perks!",
        usage="vote",
        aliases=["v"],
    )
    async def vote(self, ctx):
        embed = Embed(
            title="Vote for Me!",
            description="**By voting for me, you will:**\n- Support my development!\nUnlock Voter-only perks such as AI that remembers conversations!\n**Vote for me **[here](https://top.gg/bot/766818911505088514/vote)!",
            color=disnake.Color.green(),
        )
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="changelog",
        description="The bot's changelog.",
        aliases=["changes"],
        usage="changelog",
    )
    async def changelog(self, ctx):
        embed = Embed(
            title="v2020.12.12 Changelog",
            description="- Fixed `whois` glitch\n- Added queue support for music\n- Fixed music commands\n- **Please excuse the large help menu, I'm working on getting it to be a reaction menu!**",
            color=disnake.Color.green(),
        )
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="privacypolicy",
        description="Gives megaton's privacy policy.",
        aliases=["privacy-policy", "privpolicy", "privacy_policy", "privacy"],
        usage="privacy",
    )
    async def privacy(self, ctx):
        embed = Embed(title="megaton Privacy Policy", color=disnake.Color.green())
        embed.add_field(
            name="What information is stored?",
            value="Currently, very little information is stored. The only stored data is through our economy system and per-server settings, which will store your ID/Guild ID. All commands are logged with a username and guild name, neither your discriminator nor your ID be stored in this manner.",
        )
        embed.add_field(
            name="Questions or Concerns",
            value="If you are concerned about the data stored Join the [megaton Support Server](https://discord.gg/bNtj2nFnYA) or DM [thrzl](https://thrzl.xyz)",
        )
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url
        )
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="invite", description="Get megaton's invite link!", usage="invite"
    )
    async def invite(self, ctx):
        embed = Embed(
            title="Invite Link",
            description="The invite link of megaton!",
            color=disnake.Color.green(),
        )
        embed.set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/BFryzY8e6UbmufD_CPv815Np4QDxV2ryFGMxAoG6_YY/%3Fsize%3D1024/https/cdn.discordapp.com/icons/773162574752514049/6286d1102dc77a456919ef40bea8b198.webp?width=454&height=454"
        )
        embed.add_field(
            name="Link:",
            value="https://discord.com/api/oauth2/authorize?client_id=766818911505088514&permissions=268823622&scope=bot",
        )
        embed.set_footer(
            icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}"
        )
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="credits",
        description="Shows all the people who made this bot possible!",
        usage="credits",
    )
    async def credits(self, ctx):
        embed = Embed(
            title="Credits",
            description="This bot was created, hosted, and maintained by <@536644802595520534>. ",
            color=disnake.Color.dark_purple(),
        )
        await ctx.response.send_message(embed=embed)

    @slash_command(name="ping", description="Returns the bot ping.")
    async def ping(self, ctx):
        await ctx.response.send_message(
            f"**Pong!** Ping is {round(self.bot.latency * 1000)}ms."
        )

    @slash_command(
        name="about",
        description="Gives information about the bot.",
        usage="about",
        aliases=["info"],
    )
    async def about(self, ctx):
        embed = Embed(title="ℹ information", color=disnake.Color.green())
        embed.add_field(
            name="<:python:783034338228043797> python version",
            value=f"running python {sys.version[:5]}",
        )
        embed.add_field(
            name="<:disnake:783347864259919935> discord.py version",
            value=f"running disnake {disnake.__version__}",
        )
        embed.add_field(name="⚛ bot version", value="v2020.12.8")
        embed.add_field(name="🌐 latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(
            name="💬 command information",
            value=f"**{len(self.bot.slash_commands)}** commands in a total of **{len(self.bot.cogs)}** cogs.",
        )
        mc = 0
        for g in self.bot.guilds:
            mc += g.member_count
        embed.add_field(
            name="stats",
            value=f"bot is in {len(self.bot.guilds)} guilds and has a total of {mc} users.",
        )
        embed.add_field(name="credits", value="created by [thrzl](https://thrzl.xyz/)")
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="support", description="Get a link to the support server", usage="support"
    )
    async def support(self, ctx):
        embed = Embed(
            title="Get Support",
            description="Get support for the bot.",
            color=disnake.Color.green(),
        )
        embed.set_thumbnail(
            url="https://images-ext-1.discordapp.net/external/BFryzY8e6UbmufD_CPv815Np4QDxV2ryFGMxAoG6_YY/%3Fsize%3D1024/https/cdn.discordapp.com/icons/773162574752514049/6286d1102dc77a456919ef40bea8b198.webp?width=454&height=454"
        )
        embed.add_field(
            name="megaton Support Server",
            value="Join our [support server](https://discord.gg/bNtj2nFnYA) for assistance with the bot!",
        )
        await ctx.response.send_message("Check your DMs!")
        await ctx.message.add_reaction("📬")
        await ctx.author.send(embed=embed)


def setup(bot):
    bot.add_cog(Bot_Info(bot))
