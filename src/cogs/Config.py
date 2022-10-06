from disnake.ext import commands
import discord
import asyncio
import time
from disnake.ext.commands.converter import RoleConverter, TextChannelConverter
from bot import Atomic


class Config(commands.Cog):
    def __init__(self, bot: Atomic):
        self.bot = bot
        self.db = bot.db["settings"]

    @commands.group(
        invoke_without_subcommand=True,
        description="Edit the bot's settings in your server!",
        usage="config",
    )
    @commands.has_permissions(manage_guild=True)
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            ginfo = {"_id": ctx.guild.id}
            if await self.db.count_documents(ginfo) == 0:
                gconfig = {
                    "_id": ctx.guild.id,
                    "leveling": "Disabled",
                    "Logging": "Disabled",
                    "Welcoming": "Disabled",
                    "prefix": "k!",
                }
                await self.db.insert_one(gconfig)
            g = await self.db.find_one(ginfo)
            embed = disnake.Embed(title="Configuration Options")
            if g["leveling"] == "Enabled":
                emojistring = "<:yesx:780189815026352128><:yescheck:780189814967238656>"
            else:
                emojistring = "<:nox:780198268390604801><:nocheck:780198268268445737>"
            embed.add_field(name="1️⃣ Leveling System", value=emojistring)

            if g["Welcoming"] != "Disabled":
                channel = ctx.guild.get_channel(int(g["Welcoming"]))
                embed.add_field(name="2️⃣ Welcome messages", value=channel.mention)
            else:
                embed.add_field(
                    name="2️⃣ Welcome messages",
                    value="<:nox:780198268390604801><:nocheck:780198268268445737>",
                )

            if g["autorole"] != "Disabled":
                print(g["autorole"])
                role = ctx.guild.get_role(int(g["autorole"]))
                embed.add_field(name="3️⃣ Autorole", value=role.mention)
            else:
                embed.add_field(
                    name="3️⃣ Autorole",
                    value="<:nox:780198268390604801><:nocheck:780198268268445737>",
                )

            embed.set_footer(text="This menu will time out in 60 seconds.")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("1️⃣")
            await msg.add_reaction("2️⃣")
            await msg.add_reaction("3️⃣")
            await msg.add_reaction("❌")
            # await msg.add_reaction("3️⃣")
            def check(reaction):
                acceptedemoji = ["❌", "1️⃣", "2️⃣", "3️⃣"]
                return (
                    reaction.member == ctx.author
                    and reaction.message_id == msg.id
                    and str(reaction.emoji) in acceptedemoji
                )

            try:
                payload = await self.bot.wait_for(
                    "raw_reaction_add", timeout=60.0, check=check
                )
            except:
                await msg.edit(content="This embed has timed out.")
            else:
                gc = await self.db.find_one({"_id": ctx.guild.id})
                olevel = gc["leveling"]
                owelcome = gc["Welcoming"]
                if str(payload.emoji) == "1️⃣":
                    embed = disnake.Embed(
                        title="leveling Enabled", color=discord.Color.green()
                    )
                    if olevel == "Disabled":
                        await self.db.update_one(
                            {"_id": ctx.guild.id}, {"$set": {"leveling": "Enabled"}}
                        )
                        await ctx.send("Enabled Leveling in this guild!")
                    elif olevel == "Enabled":
                        await self.db.update_one(
                            {"_id": ctx.guild.id}, {"$set": {"leveling": "Disabled"}}
                        )
                        await ctx.send("Disabled Leveling in this guild!")
                elif str(payload.emoji) == "2️⃣":
                    embed = disnake.Embed(
                        title="Welcome Setup",
                        description="Which channel would you like welcome/leave messages to go in?",
                        color=discord.Color.green(),
                    )
                    embed.set_footer(
                        text="Make sure you use channel mentions or IDs! Type disable to turn off welcoming!"
                    )
                    msg2 = await ctx.send(embed=embed)

                    def check(m):
                        return m.author == ctx.author and m.channel == ctx.channel

                    tries = 0
                    while True:
                        wc = await self.bot.wait_for("message", check=check)
                        try:
                            if wc.content.lower().startswith("d"):
                                await self.db.update_one(
                                    {"_id": ctx.guild.id},
                                    {"$set": {"Welcoming": "Disabled"}},
                                )
                                await ctx.send("Disabled welcoming in this guild!")
                                return
                            channel = await TextChannelConverter().convert(
                                ctx, wc.content
                            )
                            wcid = channel.id
                            break
                        except:
                            if tries >= 3:
                                await ctx.send("Setup menu canceled. Please try again.")
                                return
                            tries += 1
                            await ctx.message.add_reaction("❌")
                            await ctx.send(
                                "That was an invalid channel! Please try again."
                            )
                    await self.db.update_one(
                        {"_id": ctx.guild.id}, {"$set": {"Welcoming": wcid}}
                    )
                    wcm = ctx.guild.get_channel(wcid)
                    await ctx.send(f"Set the welcome channel to {wcm.mention}!")
                    embed = disnake.Embed(
                        title="Welcome Channel",
                        description="This is now the guild welcome channel.",
                    )
                    await wcm.send(embed=embed)
                    await msg.delete()
                    await asyncio.sleep(5)
                    await msg2.delete()
                elif str(payload.emoji) == "3️⃣":
                    embed = disnake.Embed(
                        title="Autorole Setup",
                        description="Which role would you like new members to recieve when they join?",
                        color=discord.Color.green(),
                    )
                    embed.set_footer(
                        text="Make sure you use role mentions, IDs, or names!"
                    )
                    prompt = await ctx.send(embed=embed)

                    def check(m):
                        return m.author == ctx.author

                    tries = 0
                    while True:
                        rolemsg = await self.bot.wait_for("message", check=check)
                        role = rolemsg.content
                        try:
                            if role.lower().startswith("d"):
                                await self.db.update_one(
                                    {"_id": ctx.guild.id},
                                    {"$set": {"autorole": "Disabled"}},
                                )
                                break
                            else:
                                role = await RoleConverter().convert(ctx, role)
                                roleid = role.id
                                await self.db.update_one(
                                    {"_id": ctx.guild.id},
                                    {"$set": {"autorole": roleid}},
                                )
                                await ctx.send(f"Set autorole to {role.name}")
                                break
                        except:
                            try:
                                role = ctx.guild.get_role(int(role))
                                await self.db.update_one(
                                    {"_id": ctx.guild.id},
                                    {"$set": {"autorole": role.id}},
                                )
                                await ctx.send(f"Set autorole to {role.name}!")
                                break
                            except:
                                if tries >= 3:
                                    await ctx.send(
                                        "Setup menu canceled. Please try again."
                                    )
                                    return
                                tries += 1
                                await rolemsg.add_reaction("❌")
                                await ctx.send(
                                    "That was an invalid role! Please try again."
                                )

                elif str(payload.emoji) == "❌":
                    await msg.delete()
                    await ctx.message.delete()


def setup(bot):
    bot.add_cog(Config(bot))
