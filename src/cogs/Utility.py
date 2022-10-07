from disnake.ext import commands
from disnake.ext.commands import slash_command
from disnake import Member, Color, Asset, PartialEmoji
from datetime import date, timedelta, datetime
import os
import random
import aiohttp
import aiofiles
from aiohttp import *
from colorthief import ColorThief
import json
import asyncio
from disnake.ext.commands.slash_core import ApplicationCommandInteraction
from bot import Embed


async def get_color(img):
    clr_thief = ColorThief(img)
    dominant_color = clr_thief.get_color(quality=1)
    return dominant_color


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name="translate",
        description="Translates text with language",
        usage="translate <text>",
        aliases=["tr"],
    )
    async def translate(self, ctx: ApplicationCommandInteraction, *, message):
        await ctx.response.defer()
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://bruhapi.xyz/translate/{message}")
            rej = await response.json()
            text = rej["text"]
            lang = rej["lang"]
            embed = Embed(title=f":flag_{lang}: Translation:", description=text)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @slash_command(
        name="server",
        description="Returns information about the current guild.",
        aliases=["guild"],
        usage="invite",
    )
    async def server(self, ctx: ApplicationCommandInteraction):
        await ctx.response.defer()
        url = ctx.guild.icon
        await url.save(f"{ctx.guild.id}av.png", seek_begin=True)
        clr = ", ".join(await get_color(f"{ctx.guild.id}av.png"))
        os.remove(f"{ctx.guild.id}av.png")
        red, blue, green = [int(c) for c in clr]
        color = Color.from_rgb(red, green, blue)
        tcount = len(ctx.guild.text_channels)
        vcount = len(ctx.guild.voice_channels)
        rcount = len(ctx.guild.roles)
        embed = Embed(title=ctx.guild.name + " Server Information", color=color)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(
            name="Region <a:greyscaleearth:777565668442374245>",
            value=ctx.guild.region,
            inline=True,
        )
        embed.add_field(
            name="Member Count",
            value=f"<:member:779742587425652757> {ctx.guild.member_count}",
            inline=True,
        )
        embed.add_field(
            name="Channel Count",
            value=f"<:channel:779742587497742376> {tcount} | <:voicechannel:779742587011465238> {vcount}",
        )
        embed.add_field(name="Role Count 🎨", value=f"{rcount}")
        embed.add_field(name="Top Role ✨🎨", value=ctx.guild.roles.reverse()[0])
        embed.add_field(name="Creation Date 📅", value=ctx.guild.created_at)
        embed.set_footer(
            icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}"
        )
        await ctx.send(embed=embed)

    @slash_command(
        name="suggest",
        description="Report a bug or make a suggestion to the developers.",
        aliases=["suggestion", "bugreport", "bug"],
        usage="suggest <suggestion>",
    )
    async def suggest(self, ctx: ApplicationCommandInteraction, *, suggestion="0"):
        if suggestion == "0":
            embed = Embed(
                title="Suggestion", description="What do you want to suggest?"
            )
            embed.set_footer(
                text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
            )
            sug = await ctx.send(embed=embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            suggestion = await self.bot.wait_for("message", check=check)
            await sug.add_reaction("📨")
        else:
            await ctx.message.add_reaction("📨")
        embed = Embed(title="New Suggestion", description=suggestion)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
        suggestchannel = await self.bot.fetch_channel(779112252833792081)
        await suggestchannel.send(embed=embed)

    @slash_command(
        name="giveaway",
        description="Starts a giveaway in the current channel.",
        case_insensitive=True,
        aliases=["gws"],
    )
    @commands.has_guild_permissions(administrator=True)
    async def gstart(
        self, ctx: ApplicationCommandInteraction, time="none", *, prize="none"
    ):
        if time == "none":
            embed = Embed(
                title="Giveaway Setup 🎉",
                description="How long should the giveaway last?",
                color=ctx.author.color,
            )
            embed.set_footer(text="Use values like 7d, 10m, 30s, or 1h.")
            msg = await ctx.send(embed=embed)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            try:
                m = await self.bot.wait_for("message", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You didn't answer in time!")
            else:
                time = m.content

                await m.delete()
                embed = Embed(
                    title="Giveaway Setup 🎉", description="What's the giveaway prize?"
                )
                await msg.edit(embed=embed)

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                try:
                    m2 = await self.bot.wait_for("message", timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send("You didn't answer in time!")
                else:
                    prize = m2.content

                    await m2.delete()
                    await msg.delete()
        elif time != "none" and prize == "none":
            embed = Embed(
                title="Giveaway Setup 🎉",
                description="What's the giveaway prize?",
                color=ctx.author.color,
            )
            msg = await ctx.send(embed=embed)

            def check(m):
                return (
                    type(m.content) == "str"
                    and m.channel == ctx.channel
                    and m.author == ctx.author
                )

            try:
                m = await self.bot.wait_for("message", timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("You didn't answer in time!")
            else:
                prize = m.content
                await m.delete()
                await msg.delete()
        seconds = 0
        embed1 = Embed(title="🎉New **Giveaway!**", description=prize)
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{int(time) // 60 // 60 // 24} days"
            end = datetime.now() + timedelta(days=seconds)
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{int(time) // 60 // 60} hours"
            end = datetime.now() + timedelta(hours=seconds)
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{int(time) // 60} minutes"
            end = datetime.now() + timedelta(minutes=seconds)
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{time} seconds"
            end = datetime.now() + timedelta(seconds=seconds)
        if seconds == 0:
            embed = Embed(
                title="Warning",
                description="Please specify a proper duration. Example: `10d`, `5m`, etc.",
            )
        elif seconds > 7776000:
            embed = Embed(
                title="Warning",
                description="You have specified a too long duration!\nMaximum duration is 90 days.",
            )
        if seconds != 0 or seconds < 7776000:
            formatendtime = end.strftime("%H:%M on %B %d, %Y")
            embed1.add_field(
                name="Ends at: ", value=f"{formatendtime} UTC", inline=True
            )
            embed1.set_footer(text=f"Ends {counter} from now.")
            gwembed = await ctx.send(embed=embed1)
            await gwembed.add_reaction("🎉")
            channel = gwembed.channel
            await asyncio.sleep(seconds)
            gwembedmsg = await channel.fetch_message(gwembed.id)
            users = await gwembedmsg.reactions[0].users().flatten()
            users.pop(users.index(self.bot.user))
            today = date.today()
            todaystr = today.strftime("%B %d, %Y")
            winner = random.choice(users)
            embed2 = Embed(
                title=f"The giveaway for **{prize}** has ended.",
                description=f"Ended on {todaystr}",
                color=ctx.author.color,
            )
            embed2.set_footer(
                icon_url=winner.avatar.url, text=f"{winner.name} won this giveaway."
            )
            embed = Embed(
                title="**Giveaway Winner!**",
                description=f"{winner.mention}, you just won **{prize}** in **{ctx.guild.name}**!",
                color=winner.color,
            )
            await winner.send(embed=embed)
            await ctx.send(f"Congrats to {winner.mention} for winning {prize}!")
            await gwembedmsg.edit(embed=embed2)

    @slash_command(
        name="raw", description="Prints raw text in a codeblock.", usage="raw <text>"
    )
    async def raw(self, ctx: ApplicationCommandInteraction, *, msg):
        await ctx.send(f"```{msg}```")

    @slash_command(
        name="pokedex",
        description="Gets information on a Pokemon!",
        usage="pokemon <pokemon>",
        aliases=["pk", "pdx", "pd", "pokemon"],
    )
    async def pokemon(self, ctx: ApplicationCommandInteraction, *, pokemon):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                f"https://some-random-api.ml/pokedex?pokemon={pokemon}"
            )
            if str(response.status) == "404":
                await ctx.send("I couldn't find that pokemon. Please try again.")
            else:
                rj = await response.json()
                name = (rj["name"]).capitalize()
                pid = rj["id"]
                ptype = rj["type"]
                desc = rj["description"]
                species = rj["species"]
                stats = rj["stats"]
                evolfam = rj["family"]
                evs = evolfam["evolutionLine"]
                evs = str(evs)
                evs = evs.replace("'", "")
                evs = evs.replace("]", "")
                evs = evs.replace("[", "")
                hp = stats["hp"]
                attack = stats["attack"]
                defense = stats["defense"]
                speed = stats["speed"]
                spattack = stats["sp_atk"]
                spdef = stats["sp_def"]
                abilities = rj["abilities"]
                abilities = str(abilities)
                abilities = abilities.replace("'", "")
                abilities = abilities.replace("[", "")
                abilities = abilities.replace("]", "")
                weight = rj["weight"]
                height = rj["height"]
                weight = weight.replace("\xa0", " ")
                height = height.replace("\xa0", " ")
                species = str(species)
                species = species.replace("'", "")
                species = species.replace("[", "")
                species = species.replace("]", "")
                species = species.replace(",", "")
                ptype = str(ptype)
                ptype = ptype.replace("'", "")
                ptype = ptype.replace("[", "")
                ptype = ptype.replace("]", "")
                imgs = rj["sprites"]
                if int(rj["generation"]) < 6:
                    img = imgs["animated"]
                else:
                    img = imgs["normal"]
                url = imgs["normal"]
                try:
                    f = await aiofiles.open(f"{pokemon}av.png", mode="wb")
                    idx = await session.get(url)
                    data = await idx.read()
                    await f.write(data)
                    await f.close()
                    # await url.save(f'{pokemon}av.png',seek_begin = True)
                    clr = await get_color(f"{pokemon}av.png")
                    os.remove(f"{pokemon}av.png")
                    clr = str(clr).replace("(", "")
                    clr = str(clr).replace(")", "")
                    clr = clr.split(", ")
                    red = int(clr[0])
                    blue = int(clr[2])
                    green = int(clr[1])
                    color = Color.from_rgb(red, green, blue)
                    embed = Embed(title=name, description=desc, color=color)
                except:
                    embed = Embed(title=name, description=desc)
                embed.set_image(url=img)
                embed.add_field(
                    name="Information",
                    value=f"ID: {pid}\nThe {species}\nFirst introduced in generation {(rj['generation'])}\nType(s): {ptype}\nHeight: {height}\nWeight: {weight}\nAbilities: {abilities}",
                    inline=False,
                )
                embed.add_field(
                    name="Base Stats",
                    value=f"HP: {hp}\nDefense: {defense}\nSpeed: {speed}\nAttack: {attack}\nSpecial Attack: {spattack}\nSpecial Defense: {spdef}",
                )
                if len(evs) != 0:
                    embed.add_field(name="Evolution Line", value=evs, inline=False)
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        for u in message.mentions:
            if (u.display_name[:5]) == "[AFK]":
                embed = Embed(
                    title="AFK Alert", description=f"{u.display_name} is AFK."
                )
                await message.channel.send(embed=embed)

    @slash_command(name="afk")
    async def afk(self, ctx):
        oldn = ctx.author.display_name
        await ctx.author.edit(reason="AFK", nick=f"[AFK] {oldn}")
        embed = Embed(
            title="AFK",
            description="You have been marked as AFK. Any user who tries to mention you will get a notice saying that you are away.",
        )
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.author

        msg = await self.bot.wait_for("message", check=check)
        await ctx.author.edit(reason="User is no longer AFK", nick=oldn)
        await msg.channel.send("You have been unmarked as AFK.")

    @slash_command(
        name="remind",
        description="Sets a reminder",
        case_insensitive=True,
        aliases=["remindme", "remind_me"],
    )
    async def reminder(self, ctx: ApplicationCommandInteraction, time, *, reminder):
        user = ctx.message.author
        embed = Embed(color=0x55A7F7, timestamp=datetime.utcnow())
        seconds = 0
        if reminder is None:
            embed.add_field(
                name="Warning",
                value="Please specify what do you want me to remind you about.",
            )  # Error message
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"
        if seconds == 0:
            embed.add_field(
                name="Warning",
                value="Please specify a proper duration. Example: `10d`, `5m`, etc send `reminder_help` for more information.",
            )
        elif seconds > 7776000:
            embed.add_field(
                name="Warning",
                value="You have specified a too long duration!\nMaximum duration is 90 days.",
            )
        else:
            await ctx.message.add_reaction("⏱")
            await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
            await asyncio.sleep(seconds)
            await ctx.author.send(
                f"Hi, you asked me to remind you about {reminder} {counter} ago."
            )
            return
        await ctx.send(embed=embed)

    @slash_command(name="stats", description="Gives you bot stats!", usage="stats")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def stats(self, ctx):
        async with aiohttp.ClientSession() as session:
            r = await session.get("https://api.statcord.com/v3/766818911505088514")
        data = await r.text()
        data = json.loads(data)
        pdata = data["data"]
        for d in pdata:
            usercount = d["users"]
            cpu = d["cpuload"]
        embed = Embed(
            title="atomic Stats",
            description="My official stats!",
        )
        embed.add_field(name="Server Count", value=len(self.bot.guilds))
        embed.add_field(name="User Count", value=f"{usercount}")
        embed.add_field(name="CPU Load", value=f"{cpu}%")
        embed.set_footer(
            icon_url="https://cdn.statcord.com/logo.png", text=f"Powered by Statcord"
        )
        await ctx.send(embed=embed)

    @slash_command(
        name="whois",
        description="Returns information about the current user.",
        aliases=["profile", "ui"],
        usage="whois <mention>",
    )
    async def whois(self, ctx: ApplicationCommandInteraction, *, member: Member = None):
        m: Member = member or ctx.author
        await ctx.response.defer()
        url: Asset = m.avatar
        await url.save(f"{m.id}av.png", seek_begin=True)
        clr = await get_color(f"{m.id}av.png")
        os.remove(f"{m.id}av.png")
        clr = str(clr).replace("(", "")
        clr = str(clr).replace(")", "")
        clr = clr.split(", ")
        red = int(clr[0])
        blue = int(clr[2])
        green = int(clr[1])
        color = Color.from_rgb(red, green, blue)
        flags = m.public_flags
        flagsstr = ""
        if flags.staff:
            flagsstr = flagsstr + " <:staff:787444950974988288>"
        if flags.hypesquad:
            flagsstr = flagsstr + " <:hypeevents:787445731782688779>"
        if flags.early_supporter:
            flagsstr = flagsstr + " <:earlysupporter:787446049102102559>"
        if flags.bug_hunter or flags.bug_hunter_level_2:
            flagsstr = flagsstr + " <:bughunter:787446945098367046>"
        if flags.hypesquad_brilliance:
            flagsstr = flagsstr + " <:brilliance:786217607065108481>"
        if flags.hypesquad_bravery:
            flagsstr = flagsstr + " <:bravery:786217999802957835>"
        if flags.hypesquad_balance:
            flagsstr = flagsstr + " <:balance:786217943900880916>"
        if flags.verified_bot_developer:
            flagsstr = flagsstr + " <:verifiedbotdev:787449074994380821>"
        if flagsstr != "":
            embed = Embed(title=m.name, description=flagsstr, color=color)
        else:
            embed = Embed(title=m.name, description=flagsstr, color=color)
        embed.set_thumbnail(url=m.avatar.url)
        embed.add_field(name="ID", value=m.id, inline=True)
        embed.add_field(name="Created on: ", value=m.created_at.date(), inline=True)
        embed.add_field(name="Joined on: ", value=m.joined_at.date(), inline=True)
        embed.add_field(name="Highest Role", value=m.top_role.mention, inline=True)
        roles = [role.mention for role in m.roles if role.name != "@everyone"]
        roles.reverse()
        ", ".join(roles)
        embed.add_field(name="Roles", value=roles, inline=True)
        embed.set_footer(
            icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}"
        )
        await ctx.send(embed=embed)

    @slash_command(
        name="pip",
        description="Search for a package on PyPi!",
        usage="pip <package>",
        aliases=["pypi", "pypa"],
    )
    async def pip(self, ctx: ApplicationCommandInteraction, *, package):
        datal = ["author", "description", "downloads", "home_page", "name", "summary"]
        async with aiohttp.ClientSession() as session:
            package = str(package).lower()
            package = package.replace(" ", "-")
            r = await session.get(f"https://pypi.org/pypi/{package}/json")
            if str(r.status) == "404":
                embed = Embed(
                    title="Package not found...",
                    description="Make sure that you use full package names and that you are asking about a valid package!",
                    color=Color.red(),
                )
                await ctx.send(embed=embed)
            else:
                data = await r.json()
                pkginfo = data["info"]
                author = pkginfo["author"]
                downloads = pkginfo["downloads"]
                lic = pkginfo["license"]
                url = pkginfo["project_url"]
                name = pkginfo["name"]
                summary = pkginfo["summary"]
                ver = pkginfo["version"]
                req = pkginfo["requires_dist"]
                req = str(req)
                req = req.replace("[", "")
                req = req.replace("]", "")
                req = req.replace('"', "`")
                req = req.replace("'", "`")
                embed = Embed(
                    title=name,
                    description=summary,
                    url=url,
                )
                embed.set_thumbnail(
                    url="https://pypi.org/static/images/logo-small.6eef541e.svg"
                )
                t = await session.get(f"https://pypi.org/user/{author}/")
                if int(t.status) != 404:
                    embed.set_author(
                        name=f"Created by {author}",
                        url=f"https://pypi.org/user/{author}/",
                    )
                else:
                    embed.set_author(name=f"Created by {author}")
                embed.add_field(name="Latest Version", value=ver)
                embed.add_field(name="Requirements", value=req)
                if lic != "":
                    embed.add_field(name="License", value=lic)
                await ctx.send(embed=embed)

    @slash_command(
        name="emojisteal",
        description="Steals an emoji from another server!",
        usage=f"emojisteal <emoji> <name>",
    )
    async def emojisteal(
        self, ctx: ApplicationCommandInteraction, emoji: PartialEmoji, name
    ):
        await ctx.response.defer()
        img = await emoji.read()
        em = await ctx.guild.create_custom_emoji(name=name, image=img)
        embed = Embed(
            title=f"Emoji <:{em.name}:{em.id}> [`:{em.name}:`] was added successfully!",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Utility(bot))
