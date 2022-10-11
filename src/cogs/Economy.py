from disnake.ext.commands.core import cooldown, Cog
from disnake.ext.commands.cooldowns import BucketType
from disnake import Member
from random import randint, choice
from disnake.ext.commands.slash_core import ApplicationCommandInteraction, slash_command
from bot import Megaton, Embed
from db import EconomyData

from utils.data import Economy as _eco


class Economy(Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
        self.data = _eco

    @slash_command(name="rob", description="rob a user!")
    @cooldown(1, 120, BucketType.user)
    async def rob(self, ctx: ApplicationCommandInteraction, member: Member):
        choice = randint(0, 1)
        user = await EconomyData.get(member.id)
        victim = await EconomyData.get(ctx.author.id)

        if victim["wallet"] >= user["wallet"]:
            high = int(user["wallet"])
        elif victim["wallet"] < user["wallet"]:
            high = int(victim["wallet"])
        amt = randint(0, high)

        if choice == 1:
            await EconomyData.update_wallet(member.id, -amt)
            await EconomyData.update_wallet(ctx.author.id, amt)
            await ctx.response.send_message(
                embed=Embed(
                    description=f"**{ctx.author.name}** just stole **{amt}** coins from **{member.name}**!"
                ).set_author(name="robbed!")
            )
        else:
            await EconomyData.update_wallet(ctx.author.id, -amt)
            await ctx.response.send_message(
                f"**{ctx.author.name}** just tried to rob **{member.name}**, but was caught! they paid a **{amt}** coins fine."
            )

    @slash_command(name="work", description="work for some coins!", usage="work")
    @cooldown(1, 360, BucketType.user)
    async def work(self, ctx):
        money = randint(0, 3000)
        embed = Embed(
            description=f"you worked as a **{choice(self.data.work.jobs)}** and earned **{money} coins**"
        ).set_author(name=choice(self.data.work.job_worked))
        await EconomyData.update_wallet(ctx.author.id, money)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        aliases=["dep", "bank"],
        name="deposit",
        description="deposit some money into your bank account!",
        usage="deposit <money>",
    )
    @cooldown(1, 600, BucketType.user)
    async def dep(self, ctx: ApplicationCommandInteraction, amt: int):
        user = await EconomyData.get(ctx.author.id)
        if (user.wallet) < amt:
            await ctx.response.send_message(
                "You don't have enough money in your wallet for that!"
            )
        else:
            await EconomyData.deposit(ctx.author.id, amt)
            await ctx.response.send_message(
                f"You just deposited **{amt}** coins into your bank account!"
            )

    @slash_command(
        name="withdraw",
        description="withdraw coins from your bank account!",
        usage="withdraw <number>",
        aliases=["with"],
    )
    @cooldown(1, 10, BucketType.user)
    async def withdraw(self, ctx: ApplicationCommandInteraction, amt: int):
        user = await EconomyData.get(ctx.author.id)
        if (user["bank"]) < amt:
            await ctx.response.send_message(
                "You don't have enough money in the bank for that!"
            )
        else:
            await EconomyData.withdraw(ctx.author.id, amt)
            await ctx.response.send_message(
                f"You just withdrew **{amt}** coins from your bank account!"
            )

    @slash_command(name="beg", description="beg strangers for money!", usage="beg")
    @cooldown(1, 30, BucketType.user)
    async def beg(self, ctx):
        c = randint(0, 1)
        donor = choice(self.data.beg.people)
        if c == 1:
            guild = ctx.guild
            guild = guild.id
            money = randint(34, 120)
            await EconomyData.update_wallet(ctx.author.id, money)
            await ctx.response.send_message(
                embed=Embed(
                    description=f"**{donor}** just gave you **{money}** coins!"
                ).set_author(name=choice(self.data.beg.messages))
            )
        else:
            await ctx.response.send_message(
                embed=Embed(
                    description=f"{donor}: {choice(self.data.beg.deny_messages)}"
                ).set_author(name=donor)
            )

    @slash_command(
        name="balance",
        description="check your balance!",
        usage="balance [user]",
        aliases=["bal", "money", "cash"],
    )
    async def balance(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        user = await EconomyData.get(member.id)
        walletamt = user.wallet
        bankamt = user.bank
        embed = (
            Embed()
            .set_author(
                name=f"{member.name}'s balance", icon_url=member.display_avatar.url
            )
            .set_thumbnail(
                url=member.avatar.url if member.avatar else member.default_avatar.url
            )
        )
        embed.add_field(name="wallet", value=f"{walletamt} coins")
        embed.add_field(name="bank", value=f"{bankamt} coins")
        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
