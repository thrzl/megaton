from disnake.ext import commands, tasks
import dbl

from disnake.ext import commands

import dbl


class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc2NjgxODkxMTUwNTA4ODUxNCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA2MzI0Mjc5fQ.ADjcN7pcHL9D5lfnGYHPQH8lXQyvqxzcWg7jSHLIgrs"  # set this to your DBL token
        self.dblpy = dbl.DBLClient(
            self.bot,
            self.token,
            webhook_path="/dblwebhook",
            webhook_auth="password",
            webhook_port=5000,
        )

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        print("Received an upvote:", "\n", data, sep="")

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        print("Received a test upvote:", "\n", data, sep="")


def setup(bot):
    bot.add_cog(TopGG(bot))
