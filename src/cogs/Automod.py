from disnake.ext import commands
import discord

mongo_url = "mongodb+srv://admin:4n0tS0g00D1ne@sentry.z5zvv.mongodb.net/Reliex?retryWrites=true&w=majority"
from disnake.utils import get


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for word in filtered_words:
            if word in message.content:
                await message.delete()
            try:
                await message.author.send("Don't use that word.")
            except:
                await message.channel.send(
                    f"{message.author.mention}, don't use that word."
                )
        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(Automod(bot))
