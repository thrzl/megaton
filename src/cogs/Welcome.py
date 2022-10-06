from disnake.ext import commands
import discord
import random
from pymongo import MongoClient
import os
from colorthief import ColorThief

mongo_url = "mongodb+srv://admin:4n0tS0g00D1ne@sentry.z5zvv.mongodb.net/Reliex?retryWrites=true&w=majority"
cluster = MongoClient(mongo_url)
db = cluster["Sentry"]
collection = db["settings"]


async def get_color(img):
    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)
    return dominant_color


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        wcc = collection.find_one({"_id": member.guild.id})
        wc = wcc["Welcoming"]
        # eg = await self.bot.fetch_guild(member.guild.id)
        if wc != "Disabled":
            try:
                wcc = collection.find_one({"_id": member.guild.id})
                wc = wcc["Welcoming"]

            except:
                pass
            else:
                url = member.avatar_url_as(format="png")
                await url.save(f"{member.id}av.png", seek_begin=True)
                clr = await get_color(f"{member.id}av.png")
                os.remove(f"{member.id}av.png")
                clr = str(clr).replace("(", "")
                clr = str(clr).replace(")", "")
                clr = clr.split(", ")
                red = int(clr[0])
                blue = int(clr[2])
                green = int(clr[1])
                color = discord.Color.from_rgb(red, green, blue)
                welcome = member.guild.get_channel(wc)
                embed = disnake.Embed(
                    title=f"Goodbye {member.name}! 😢",
                    description=f"Thanks for visiting {member.guild.name}!",
                    color=color,
                )
                embed.set_thumbnail(url=member.avatar_url)
                await welcome.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        wcc = collection.find_one({"_id": member.guild.id})
        wc = wcc["Welcoming"]
        if wc != "Disabled":
            try:
                wcc = collection.find_one({"_id": member.guild.id})
                wc = wcc["Welcoming"]
            except:
                pass
            else:
                url = member.avatar_url_as(format="png")
                await url.save(f"{member.id}av.png", seek_begin=True)
                clr = await get_color(f"{member.id}av.png")
                os.remove(f"{member.id}av.png")
                clr = str(clr).replace("(", "")
                clr = str(clr).replace(")", "")
                clr = clr.split(", ")
                red = int(clr[0])
                blue = int(clr[2])
                green = int(clr[1])
                color = discord.Color.from_rgb(red, green, blue)
                welcome = member.guild.get_channel(int(wc))
                embed = disnake.Embed(
                    title=f"Goodbye {member.name}! 😢",
                    description=f"Thanks for visiting {member.guild.name}!",
                    color=color,
                )
                embed.set_thumbnail(url=member.avatar_url)
                await welcome.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        wcc = collection.find_one({"_id": member.guild.id})
        wc = wcc["Welcoming"]
        if wc != "Disabled":
            try:
                wcc = collection.find_one({"_id": member.guild.id})
                wc = wcc["Welcoming"]
            except:
                pass
            else:
                url = member.avatar_url_as(format="png")
                await url.save(f"{member.id}av.png", seek_begin=True)
                clr = await get_color(f"{member.id}av.png")
                os.remove(f"{member.id}av.png")
                clr = str(clr).replace("(", "")
                clr = str(clr).replace(")", "")
                clr = clr.split(", ")
                red = int(clr[0])
                blue = int(clr[2])
                green = int(clr[1])
                color = discord.Color.from_rgb(red, green, blue)
                welcome = member.guild.get_channel(int(wc))
                embed = disnake.Embed(
                    title=f"Welcome {member.name}! 🎉",
                    description=f"Welcome to {member.guild.name}!",
                    color=color,
                )
                embed.set_thumbnail(url=member.avatar_url)
                await welcome.send(embed=embed)
        wr = wcc["autorole"]
        if wr != "Disabled":
            role = member.guild.get_role(int(wr))
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        homeg = await self.bot.fetch_channel(773162576141090816)
        url = guild.icon_url_as(format="png")
        await url.save(f"{guild.id}av.png", seek_begin=True)
        clr = await get_color(f"{guild.id}av.png")
        os.remove(f"{guild.id}av.png")
        clr = str(clr).replace("(", "")
        clr = str(clr).replace(")", "")
        clr = clr.split(", ")
        red = int(clr[0])
        blue = int(clr[2])
        green = int(clr[1])
        color = discord.Color.from_rgb(red, green, blue)
        embed = disnake.Embed(
            title=f"Joined {guild.name}!",
            description=f"Guild has {guild.member_count} members and was created on {guild.created_at.now().date()}.",
            color=color,
        )
        owner = await self.bot.fetch_user(guild.owner_id)
        embed.add_field(name="Owner", value=f"{owner.name} | {guild.owner_id}")
        embed.set_thumbnail(url=guild.icon_url)
        await homeg.send(embed=embed)
        channel = random.choice(guild.channels)
        embed = disnake.Embed(
            title="Thanks for inviting me!",
            description="Thanks for inviting me to your server! If you ever need any help, just go ahead and join the official [support server](https://discord.gg/bNtj2nFnYA)!",
            color=discord.Color.green(),
        )
        await channel.send(embed=embed)
        collection = db["settings"]
        if collection.count_documents({"_id": guild.id}) == 0:
            collection.insert_one(
                {
                    "_id": guild.id,
                    "leveling": "Disabled",
                    "Welcoming": "Disabled",
                    "autorole": "Disabled",
                }
            )
        collection = db["prefixes"]
        if collection.count_documents({"_id": guild.id}) == 0:
            collection.insert_one({"_id": guild.id, "prefix": "k!"})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        url = guild.icon_url_as(format="png")
        await url.save(f"{guild.id}av.png", seek_begin=True)
        clr = await get_color(f"{guild.id}av.png")
        os.remove(f"{guild.id}av.png")
        clr = str(clr).replace("(", "")
        clr = str(clr).replace(")", "")
        clr = clr.split(", ")
        red = int(clr[0])
        blue = int(clr[2])
        green = int(clr[1])
        color = discord.Color.from_rgb(red, green, blue)
        homeg = await self.bot.fetch_channel(773162576141090816)
        embed = disnake.Embed(title=f"Left {guild.name}!", color=color)
        embed.set_thumbnail(url=guild.icon_url)
        await homeg.send(embed=embed)
        collection = db["settings"]
        collection.delete_one({"_id": guild.id})
        collection = db["leveldb"]
        collection.delete_many({"guildid": guild.id})
        collection = db["prefixes"]
        collection.delete_one({"_id": guild.id})


def setup(bot):
    bot.add_cog(Welcome(bot))
