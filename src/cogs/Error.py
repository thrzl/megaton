from disnake.ext.commands.cog import Cog
from datetime import datetime, timedelta
import traceback as tb
from disnake.ext.commands.slash_core import ApplicationCommandInteraction
from humanize import naturaldelta
from bot import Embed
from disnake.ext.commands.errors import (
    MissingPermissions,
    BotMissingPermissions,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
    BadArgument,
    CommandInvokeError,
    NSFWChannelRequired,
)


class Error(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_slash_command(self, ctx):
        time = str(datetime.now())[:-10]
        print(
            f"[{time}] {ctx.author.name} in {ctx.guild.name} ran command: {ctx.application_command.name}"
        )

    @Cog.listener()
    async def on_slash_command_error(
        self, ctx: ApplicationCommandInteraction, error
    ):  # exceptions, will add more
        if isinstance(error, MissingPermissions):
            embed = Embed(
                title="<a:suspicious:777565669860442132> **What are you trying to pull here...**",
                description=f"You don't have the correct permissions to run that command {ctx.author.name}, {error}",
            )
            await ctx.response.send_message(embed=embed)
            await ctx.message.add_reaction("❌")
        elif isinstance(error, BotMissingPermissions):
            mperm = str(error)
            mperm = mperm.replace("Bot requires", "")
            mperm = mperm.replace("permission(s) to run this command.", "")
            await ctx.response.send_message(
                f"**Uhh...** I don't have the correct permissions to do that...I'm missing the{mperm}permission."
            )
            await ctx.message.add_reaction("❌")
        elif isinstance(error, BotMissingPermissions):
            await ctx.response.send_message(
                f"**Uhh...** I don't have the correct permissions to do that...I'm missing {error.missing_perms}"
            )
            await ctx.message.add_reaction("❌")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.response.send_message(
                "**Uhh...** you missed an argument in the command..."
            )
            await ctx.message.add_reaction("❌")
        elif isinstance(error, BadArgument):
            await ctx.response.send_message(
                "**Uhh...** one of your arguments is wrong..."
            )
            await ctx.message.add_reaction("❌")
        elif isinstance(error, CommandInvokeError):
            time = str(datetime.now())[:-10]
            print(f"[{time}] ERROR: {error.original}")
            embed = Embed(
                title="<a:dontcry:777565669738151996> **Oh no...**",
                description="You've caused an error! The devs have been notified and will deal with the problem shortly.\n**Need extra help?** Join the [**Support Server**](https://discord.gg/bNtj2nFnYA)",
            )
            embed.add_field(name="error", value=f"```{error}```")
            await ctx.response.send_message(embed=embed)
            # errorc = await self.bot.fetch_channel(773162575843688497)
            # embed = Embed(
            #     title="an error occurred",
            #     description=f"caused by **{ctx.command.name}**, which was run by **{ctx.author}**\n**full usage:** `{ctx.message.content}`\nauthor id: `{ctx.author.id}` \guild id: `{ctx.guild.id}`\guild name: {ctx.guild.name}",
            # )
            # embed.add_field(name="Error", value=f"```{error}```")
            # eemb = await errorc.send(embed=embed)
            # await eemb.add_reaction("➕")

            # def check(r):
            #     return (
            #         str(r.emoji) == "➕"
            #         and r.member != ctx.me
            #         and r.message_id == eemb.id
            #     )

            # try:
            #     p = await self.bot.wait_for(
            #         "raw_reaction_add", timeout=3600.0, check=check
            #     )
            # except:
            #     pass
            # else:
            #     traceb = tb.format_exception(type(error), error, error.__traceback__)
            #     ee = ""
            #     for i in traceb:
            #         ee = ee + f"{i}"
            #     embed = Embed(
            #         title="An error occurred",
            #         description=f"Caused by **{ctx.command.name}**, which was run by **{ctx.author}**\n**Full Usage:** `{ctx.message.content}`\n**Author ID:** `{ctx.author.id}` \n**Guild ID:** `{ctx.guild.id}`\n**Guild Name:** {ctx.guild.name}",
            #     )
            #     embed.add_field(name="Error", value=f"```py\n...{ee[-1000:]}\n```")
            #     eemb = await eemb.edit(embed=embed)
        elif isinstance(error, CommandNotFound):
            pass
        elif isinstance(error, CommandOnCooldown):
            remaining = error.retry_after
            timestr = naturaldelta(timedelta(seconds=remaining))
            embed = Embed(
                title="<a:explode:777565669633294407> **slow down!**",
                description=f"you're on cooldown. wait {timestr} before using `{ctx.application_command.name}` again!",
            )
            await ctx.response.send_message(
                embed=embed
            )  # f"**Too fast!** You're on cooldown. `{ctx.message}` has a cooldown of {error.cooldown}. Wait {remaining} before trying again.")
        elif isinstance(error, NSFWChannelRequired):
            embed = Embed(
                title="<a:nonono:777565669314396220> That's an nsfw command!",
                description=f"The {ctx.application_command.name} command is nsfw! Please use it in an nsfw channel!",
            )
            await ctx.response.send_message(embed=embed)
        raise error


def setup(bot):
    bot.add_cog(Error(bot))
