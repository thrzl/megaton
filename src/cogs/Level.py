import discord
from disnake.ext import commands


class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db["leveldb"]
        self.enabled_guilds = []

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return
        collection = self.db["settings"]
        gid = message.guild.id
        ginfo = {"_id": gid}
        gconf = collection.find_one(ginfo)
        if (gconf["leveling"]) == True:
            collection = self.db["leveldb"]
            author = message.author.id
            user = {"_id": author}
            guild = message.guild
            guild = guild.id
            if collection.count_documents({}) == 0:
                user_info = {
                    "_id": author,
                    "guildid": message.guild.id,
                    "Level": 1,
                    "XP": 0,
                }
                collection.insert_one(user_info)
            if collection.count_documents(user) == 0:
                user_info = {
                    "_id": author,
                    "guildid": message.guild.id,
                    "Level": 1,
                    "XP": 0,
                }
                collection.insert_one(user_info)
                await message.author.send(
                    "Hey, you're new to my leveling system, aren't you! I've added you to the database, have a good time! :tada:"
                )
            exp = collection.find(user)
            for xp in exp:
                cur_xp = xp["XP"]
                newxp = cur_xp + 1
            collection.update_one({"_id": author}, {"$set": {"XP": newxp}}, upsert=True)
            lvl = collection.find(user)
            for level in lvl:
                lvl_start = level["Level"]
                new_level = lvl_start + 1
            if cur_xp >= round(5 * (lvl_start**4 / 5)):
                collection.update_one(
                    {"_id": author}, {"$set": {"Level": new_level}}, upsert=True
                )
                await message.channel.send(
                    f"Congrats <@{author}>, you've reached level {new_level}! 🥳"
                )

    @commands.command(name="Level", description="Check your level in this guild.")
    @commands.guild_only()
    async def xp(self, ctx: ApplicationCommandInteraction, who: discord.Member = None):
        member = who or ctx.author
        user = {"_id": member.id, "guildid": ctx.guild.id}
        user = await self.db.find_one(user)
        lv = user["Level"]
        xp = user["XP"]
        try:
            embed = Embed(
                title=f"{member.name}'s level in {ctx.guild.name}",
                description=f"XP: {xp}\nLevel: {lv}",
            )
        except:
            await ctx.send(
                "Leveling isn't enabled in this guild! enable it with `k!config`!"
            )
        else:
            embed.set_thumbnail(url=member.avatar_url)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Level(bot))
