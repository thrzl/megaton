from disnake.ext import commands

import statcord


class StatcordPost(commands.Cog, name="stat"):
    def __init__(self, bot):
        self.bot = bot
        self.key = "statcord.com-UXFwSyFGaY0b55qB6eCA"
        self.api = statcord.Client(self.bot, self.key)
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.api.command_run(ctx)


def setup(bot):
    bot.add_cog(StatcordPost(bot))
