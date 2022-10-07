from disnake.ext import commands
import discord
from random import randint, choice
from pymongo import MongoClient
from disnake.ext.commands.slash_core import ApplicationCommandInteraction

from bot import Atomic, Embed


class Economy(commands.Cog):
    def __init__(self, bot: Atomic):
        self.bot = bot
        self.db = self.bot.db["econ"]

    @commands.command(name="rob", description="Rob a user!")
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def rob(self, ctx: ApplicationCommandInteraction, *, member: discord.Member):
        choice = randint(0, 1)
        user = await self.db.find_one({"_id": ctx.author.id})
        victim = await self.db.find_one({"_id": member.id})
        if await self.db.count_documents({"_id": ctx.author.id}) == 0:
            await ctx.response.send_message(
                f"{member.name} isn't participating in our economy system yet! If they'd like to, ask them to type `k!bal`"
            )
            return
        else:
            if victim["wallet"] > user["wallet"]:
                high = user["wallet"]
            elif victim["wallet"] < user["wallet"]:
                high = victim["wallet"]
            else:
                high = user["wallet"]
            high = int(high)
            amt = randint(0, high)
            if choice == 1:
                wamt = amt - (amt * 2)
                await self.db.update_one(
                    {"_id": ctx.author.id}, {"$inc": {"wallet": amt}}
                )
                await self.db.update_one({"_id": member.id}, {"$inc": {"wallet": wamt}})
                await ctx.response.send_message(
                    f"**{ctx.author.name}** just stole **{amt}** amadola from **{member.name}**!"
                )
            else:
                wamt = amt - (amt * 2)
                await self.db.update_one(
                    {"_id": ctx.author.id}, {"$inc": {"wallet": wamt}}
                )
                await ctx.response.send_message(
                    f"**{ctx.author.name}** just tried to rob **{member.name}**, but was caught! They paid a **{amt}** amadola fine."
                )

    @commands.command(name="work", description="Work for some amadola!", usage="work")
    @commands.cooldown(1, 360, commands.BucketType.user)
    async def work(self, ctx):
        jobs = [
            "exit scammer",
            "bot dev",
            "president",
            "Youtuber",
            "pro gamer",
            "pro geimer",
            "stonks invester",
            "stock investor",
            "rapper",
            "chicken nugget",
            "meatball",
            "medical assisstant",
            "doctor",
            "fabio",
            "fake girlfriend",
            "bank robber",
            "decent person",
            "mother (**SUS!**)",
            "cripto exchangre",
            "crypto exchanger",
            "Inspiration Ninja",
            "cult leader",
            "dollar",
            "robber(?)",
            "pranker",
        ]
        job = choice(jobs)
        money = randint(0, 3000)
        jobmsg = f"You worked as a **{job}** and earned **{money} amadola**"
        if await self.db.count_documents({"_id": ctx.author.id}) == 0:
            meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
            await self.db.insert_one(meminfo)
        user = await self.db.find_one({"_id": ctx.author.id})
        await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": money}})
        await ctx.response.send_message(jobmsg)

    @commands.command(
        aliases=["dep", "bank"],
        name="deposit",
        description="Deposit some money into your bank account!",
        usage="deposit <money>",
    )
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def dep(self, ctx: ApplicationCommandInteraction, amt=0):
        if amt == 0:
            await ctx.response.send_message(
                "You forgot to tell me how much money you wanted to deposit!"
            )
        try:
            amt = int(amt)
        except ValueError:
            await ctx.response.send_message(
                "You didn't give me a number! How was I supposed to work with that?"
            )
        if await self.db.count_documents({"_id": ctx.author.id}) == 0:
            meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
            await self.db.insert_one(meminfo)
        user = await self.db.find_one({"_id": ctx.author.id})
        if (user["wallet"]) < amt:
            await ctx.response.send_message(
                "You don't have enough money in your wallet for that!"
            )
        else:
            wamt = amt - (amt * 2)
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": wamt}})
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"bank": amt}})
            await ctx.response.send_message(
                f"You just deposited **{amt}** amadola into your bank account!"
            )

    @commands.command(
        name="withdraw",
        description="Withdraw amadola from your bank account!",
        usage="withdraw <number>",
        aliases=["with"],
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def withdraw(self, ctx: ApplicationCommandInteraction, amt=0):
        if amt == 0:
            await ctx.response.send_message(
                "You forgot to tell me how much money you wanted to deposit!"
            )
        try:
            amt = int(amt)
        except ValueError:
            await ctx.response.send_message(
                "You didn't give me a number! How was I supposed to work with that?"
            )
        if await self.db.count_documents({"_id": ctx.author.id}) == 0:
            meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
            await self.db.insert_one(meminfo)
        user = await self.db.find_one({"_id": ctx.author.id})
        if (user["bank"]) < amt:
            await ctx.response.send_message(
                "You don't have enough money in the bank for that!"
            )
        else:
            wamt = amt - (amt * 2)
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"wallet": amt}})
            await self.db.update_one({"_id": ctx.author.id}, {"$inc": {"bank": wamt}})
            await ctx.response.send_message(
                f"You just withdrew **{amt}** amadola from your bank account!"
            )

    @commands.command(name="beg", description="Beg strangers for money!", usage="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        c = randint(0, 1)
        people = [
            "Joe Mama",
            "Johnathan McReynolds",
            "Leonardo DiCaprio",
            "Your mom",
            "PewDiePie",
            "Tiko",
            "peepo",
            "pepe",
        ]
        messages = [
            "you stanky",
            "no u lmao",
            "what you don't have a job?",
            "I don't speak poor",
        ]
        donor = choice(people)
        if c == 1:
            guild = ctx.guild
            guild = guild.id
            ginfo = {"_id": ctx.author.id}
            if await self.db.count_documents(ginfo) == 0:
                meminfo = {"_id": ctx.author.id, "bank": 0, "wallet": 0}
                await self.db.insert_one(meminfo)
            money = randint(34, 120)
            msg = f"**{donor}** gave {money} amadola to {ctx.author.name}!"
            user = await self.db.find_one({"_id": ctx.author.id})
            await self.db.update_one(
                {"_id": ctx.author.id}, {"$inc": {"wallet": money}}
            )
            await ctx.response.send_message(msg)
        else:
            m = choice(messages)
            await ctx.response.send_message(f"{donor}: {m}")

    @commands.command(
        name="Balance",
        description="Check your balance!",
        usage="balance [user]",
        aliases=["bal", "money", "cash"],
    )
    async def balance(
        self, ctx: ApplicationCommandInteraction, member: discord.Member = None
    ):
        member = member or ctx.author
        ginfo = {"_id": member.id}
        if await self.db.count_documents(ginfo) == 0:
            meminfo = {"_id": member.id, "bank": 0, "wallet": 0}
            await self.db.insert_one(meminfo)
        user = await self.db.find_one({"_id": member.id})
        walletamt = user["wallet"]
        bankamt = user["bank"]
        embed = Embed(title=f"{member.name}'s balance")
        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.add_field(name="Wallet", value=f"{walletamt} amadola")
        embed.add_field(name="Bank", value=f"{bankamt} amadola")
        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
