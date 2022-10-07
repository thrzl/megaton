from disnake.ext import commands
import discord
from bot import Embed


class Antispam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(
            3, 4, commands.BucketType.member
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.guild.id == 773162574752514049
            and not self.bot.get_user(message.author.id).bot
        ):
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await message.delete()
                embed = Embed(
                    title="atomic Moderation 🛡",
                    description=f"You've been warned in **{message.guild.name}** for spamming.",
                    color=discord.Color.green(),
                )
                await message.author.send(embed=embed)
            else:
                pass

            # get_context and friends here or above who knows

    # commands.Cog.listener()
    # async def on_message(self,message):
    # if not message.author.bot:
    #   filter(check, self.bot.cached_messages)
    #    pass


def setup(bot):
    bot.add_cog(Antispam(bot))
