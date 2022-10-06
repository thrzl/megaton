from disnake.ext import commands
import discord
import os

# import dbl as dblpy
import random
import sys
import subprocess
import ksoftapi
from time import sleep

from disnake.ext.commands import cog


class Bot_Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.dbl = dblpy.DBLClient(
        #     self.bot,
        #     "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NjgxODkxMTUwNTA4ODUxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MzI0Mjc5fQ.ADjcN7pcHL9D5lfnGYHPQH8lXQyvqxzcWg7jSHLIgrs",
        #     True,
        #     webhook_auth="tPL8UP3qyn9XikHOA9357QpGEEawK2bv",
        #     webhook_path="/dblhookatomic",
        # )

    @commands.command(name="toggle", usage="toggle <command>")
    @commands.is_owner()
    async def toggle(self, ctx, command):
        aliases = []
        for i in self.bot.commands:
            if i.name.lower() == command.lower() or command.lower() in i.aliases:
                if i.enabled:
                    i.update(enabled=False)
                    await ctx.response.send_message(
                        f"`{command}` disabled successfully."
                    )
                else:
                    i.update(enabled=True)
                    await ctx.response.send_message(
                        f"`{command}` enabled successfully."
                    )
                return

    @commands.command(aliases=["glist"])
    @commands.is_owner()
    async def guildlist(self, ctx):
        guilds = []
        for g in self.bot.guilds:
            guilds.append(f"{g.name} | {g.id}")
        guilds = str(guilds)
        guilds = guilds.replace("[", "")
        guilds = guilds.replace("]", "")
        guilds = guilds.replace("'", "")
        owner = await self.bot.fetch_user(536644802595520534)
        await owner.send(guilds)

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, type, *, status):
        if type.startswith("p"):
            await self.bot.change_presence(activity=discord.Game(name=status))
        if type.startswith("w"):
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name=status
                )
            )
        if type.startswith("s"):
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.streaming, name=status
                )
            )
        if type.startswith("l"):
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.listening, name=status
                )
            )
        if type.startswith("c"):
            await self.bot.change_presence(
                activity=discord.Activity(type=discord.ActivityType.custom, name=status)
            )
        await ctx.response.send_message("Status changed successfully!")

    @commands.command(
        name="restart",
        description="Reboots down the bot",
        aliases=["reboot", "refresh"],
    )  # not awaiting self.bot.close() or something
    @commands.is_owner()
    async def restart(self, ctx):
        if str(ctx.author.id) == "536644802595520534":
            await ctx.message.add_reaction("🔄")
            await ctx.response.send_message("Shutting down...")
            await self.bot.close()
            os.execv(sys.executable, ["python"] + sys.argv)
            exit
        else:
            await ctx.message.add_reaction("❌")
            await ctx.response.send_message(
                "Don't do that, a message has been sent to the owner of the bot including your ID and the command."
            )
            owner = await self.bot.fetch_user(536644802595520534)
            await owner.send(
                f"{ctx.author.mention} in {ctx.guild.name} just tried to restart."
            )

    @commands.command(
        name="load",
        description="Loads an extension.",
        usage="load <extension>",
        aliases=["reload"],
    )
    @commands.is_owner()
    async def load(self, ctx, *extensions):
        jsk = self.bot.get_cog("Jishaku")
        await jsk.jsk_load(ctx, extensions)

    @commands.command(
        name="sudo",
        description="Run a command with all permissions and bypassing all checks.",
        usage="sudo <command>",
    )
    @commands.is_owner()
    async def sudo(self, ctx, *, command):
        jsk = self.bot.get_cog("Jishaku")
        await jsk.jsk_sudo(ctx, command_string=command)

    @commands.command(
        name="shutdown", description="Shuts down the bot", aliases=["die"]
    )  # not awaiting self.bot.close() or something
    @commands.is_owner()
    async def shutdown(self, ctx):
        if str(ctx.author.id) == "536644802595520534":
            await ctx.message.add_reaction("👋🏽")
            await self.bot.change_presence(status=discord.Status.offline)
            await ctx.response.send_message("Shutting down...")
            await self.bot.close()
            exit
        else:
            await ctx.message.add_reaction("❌")
            await ctx.response.send_message(
                "Don't do that, a message has been sent to the owner of the bot including your ID and the command."
            )
            owner = await self.bot.fetch_user(536644802595520534)
            await owner.send(
                f"{ctx.author.mention} in {ctx.guild.name} just tried to shutdown."
            )


def setup(bot):
    bot.add_cog(Bot_Owner(bot))
