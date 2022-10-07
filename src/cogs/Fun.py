from typing import List
from disnake import Member, File, Color, Message
from disnake.ext.commands.cooldowns import BucketType
from disnake.ext.commands.core import cooldown, check, is_nsfw
from disnake.ext.commands.cog import Cog
from disnake.ext.commands.slash_core import slash_command
from disnake.ext.commands.slash_core import ApplicationCommandInteraction
import json
from random import choice
from utils import CategoryEmbed
import ksoftapi
from bot import Embed

# from disnake.ext.bridge.context import ApplicationCommandInteraction

kc = ksoftapi.Client("fef9dba21ffb0adbec3337bbc0ac4a6ee74dcc11")
import os
import aiofiles
from asyncdagpi.client import Client
from asyncdagpi.image_features import ImageFeatures

dc = Client("OC0VYkXzJ8yxtkm0H71x35BTJRUkcc5rNWzgGsf2qPGUrN3cATAnfDCDE24aD0Ex")
from PIL import Image
from colorthief import ColorThief
import aiohttp


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.dbl = bot.dbl
        self.snipelist: List[Message] = []

    def has_voted(self):
        def predicate(ctx):
            return self.dbl.get_user_vote(ctx.author.id)

        return check(predicate)

    # @slash_command(
    #     name="votecheck", description="Check if you can redeem your voter perks!"
    # )
    # async def votecheck(self, ctx: ApplicationCommandInteraction,member: Member = None):
    #     member = member or ctx.author
    #     if await self.dbl.get_user_vote(member.id):
    #         await ctx.response.send_message(f"{member} has voted!")
    #     else:
    #         await ctx.response.send_message(f"{member} has not voted!")

    @slash_command(
        name="dog",
        description="Returns a random dog image!",
        aliases=["doge", "doggo"],
        usage="dog",
    )
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://some-random-api.ml/facts/dog")
            factj = await response.json()
            fact = factj["fact"]
            imgres = await session.get("https://some-random-api.ml/img/dog")
            imgj = await imgres.json()
            imgurl = imgj["link"]
        dogtitle = [
            "Wurf!",
            "Woof?",
            "Arf Arf!",
            "Henlo fren!",
            "Bjork",
            "*panting sounds\*",
        ]
        dogemoji = (" 🦴", " 🐶", " 🐕", " 🐕‍🦺", " 🐾")
        title = choice(dogtitle) + choice(dogemoji)
        embed = Embed(title=title)
        embed.set_footer(text=f"Did you know? {fact}")
        embed.set_image(url=imgurl)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="cat",
        description="Returns a random cat image!",
        aliases=["kat", "kitty", "kitten"],
        usage="cat",
    )
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("http://some-random-api.ml/facts/cat") as response:
                response = await response.text()
                factj = json.loads(response)
                fact = factj["fact"]
        async with aiohttp.ClientSession() as session:
            async with session.get("http://some-random-api.ml/img/cat") as response:
                response = await response.text()
                imgj = json.loads(response)
                imgurl = imgj["link"]
        cattitle = ("mrow!", "mrow?", "mrow...", "meow!")
        catemoji = (" 🐟", " 🐱", " 🐈", " 🐕‍", " 🥫", " 🐾", " 😼")
        title = choice(cattitle) + choice(catemoji)
        embed = Embed(title=title)
        embed.set_footer(text=f"Did you know? {fact}")
        embed.set_image(url=imgurl)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="fox",
        description="Returns a random fox image!",
        aliases=["vix", "vixen", "vulpen", "foxy"],
        usage="fox",
    )
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/facts/fox") as response:
                response = await response.text()
                factj = json.loads(response)
                fact = factj["fact"]
        async with aiohttp.ClientSession() as session:
            async with session.get("https://some-random-api.ml/img/fox") as response2:
                response2 = await response2.text()
                imgj = json.loads(response2)
                imgurl = imgj["link"]
        foxtitle = ("...fox...sounds?", "what **does** the fox say???")
        foxemoji = (" 🕶", " 🐾", " 🦊")
        title = choice(foxtitle) + choice(foxemoji)
        embed = Embed(title=title)
        embed.set_footer(text=f"Did you know? {fact}")
        embed.set_image(url=imgurl)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="meme",
        description="Returns a random meme!",
        aliases=["memz"],
        usage="meme",
    )
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://meme-api.herokuapp.com/gimme") as memedata:
                memedata = await memedata.text()
                memej = json.loads(memedata)
                caption = memej["title"]
                memeurl = memej["url"]
                title = caption
                embed = Embed(title=title)
                embed.set_image(url=memeurl)
                await ctx.response.send_message(embed=embed)

    @slash_command(
        name="chat",
        description="Chat with an AI Chatbot!",
        aliases=["ai", "aiml"],
        usage="chat <message>",
    )
    @cooldown(1, 2, BucketType.user)
    async def chat(self, ctx: ApplicationCommandInteraction, message):
        await ctx.response.defer()
        async with aiohttp.ClientSession() as session:
            # if await self.dbl.get_user_vote(ctx.author.id):
            url = "https://robomatic-ai.p.rapidapi.com/api.php"
            payload = f"SessionID={ctx.author.id}&in={message}&op=in&cbid=1&cbot=1&ChatSource=RapidAPI&key=key"
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "x-rapidapi-key": "f1bd510b4dmsha9e4705c644b59fp1f4043jsn121019a642ec",
                "x-rapidapi-host": "robomatic-ai.p.rapidapi.com",
            }
            response = await session.request("POST", url, data=payload, headers=headers)
            rej = await response.json()
            re = rej["out"]
        """
        else:
            response = await session.get(f'https://bruhapi.xyz/cb/{message}')
            rej = await response.json()
            re = rej['res']
        """
        embed = CategoryEmbed(ctx, description=re)

    @slash_command(
        name="wtp", description="Play Who's that pokemon in Discord!", usage="wtp"
    )
    async def wtp(self, ctx):
        p = await dc.wtp()
        embed = Embed(title="Who's that Pokemon?", color=Color.red())
        embed.set_image(url=p.question)
        embed.set_footer(text="You have 60 seconds to answer!")
        prompt = await ctx.response.send_message(embed=embed)

        def check(m):
            return (
                m.channel == ctx.channel
                and m.author != ctx.guild.me
                and m.content.lower() == p.name.lower()
            )

        try:
            ans = await self.bot.wait_for("message", check=check, timeout=60.0)
        except:
            embed = Embed(
                title="Time's up!",
                description=f"The correct answer was {p.name}!",
                color=Color.red(),
            )
            embed.set_image(url=p.answer)
            await prompt.edit(embed=embed)
            return
        else:
            embed = Embed(
                title=f"Correct, {ans.author.name}!",
                description=f"You guessed {p.name} correctly!",
                color=Color.red(),
            )
        embed.set_image(url=p.answer)
        await prompt.edit(embed=embed)

    @slash_command(name="bad", description="Bad boy!", usage="bad [user]")
    async def bad(self, ctx: ApplicationCommandInteraction, m: Member = None):
        member: Member = m or ctx.author
        b = await dc.image_process(
            ImageFeatures.bad(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
        )
        bad = Image.open(b)
        bad.save(f"{member.id}bad.png")
        # b.close()
        file = File(f"{member.id}bad.png", filename=f"{member.id}bad.png")
        embed = Embed(title=f"Bad {member.name}! Bad!")
        embed.set_image(url=f"attachment://{member.id}bad.png")
        await ctx.response.send_message(embed=embed, file=file)
        os.remove(f"{member.id}bad.png")

    @slash_command(
        name="captcha",
        description="Captchas are so hard...",
        usage="captcha <user> <text>",
        aliases=["recaptcha"],
    )
    async def captcha(
        self, ctx: ApplicationCommandInteraction, text: str, member: Member = None
    ):
        member = member or ctx.author
        image = str(member.avatar.url if member.avatar else member.default_avatar.url)
        c = await dc.image_process(ImageFeatures.captcha(), image, text=text)
        cap = Image.open(c)
        cap.save(f"{member.id}captcha.png")
        # c.close()
        file = File(f"{member.id}captcha.png", filename=f"{member.id}captcha.png")
        await ctx.response.send_message(file=file)
        os.remove(f"{member.id}captcha.png")

    @slash_command(
        name="triggered",
        description="u mad bro?",
        usage="triggered <user>",
        aliases=["trigger"],
    )
    async def triggered(
        self, ctx: ApplicationCommandInteraction, member: Member = None
    ):
        member = member or ctx.author
        image = str(member.avatar.url if member.avatar else member.default_avatar.url)[
            :-10
        ]
        print(image)
        async with aiohttp.ClientSession() as session:
            r = await session.get(
                f"https://some-random-api.ml/canvas/triggered?avatar={image}"
            )
        f = await aiofiles.open(f"{member.id}triggered.gif", mode="wb")
        triggeredgif = await r.read()
        if int(r.status) != 200:
            await ctx.response.send_message(
                f"somethin went wrong. we're looking into it, don't worry."
            )
            return
        await f.write(triggeredgif)
        tri = Image.open(f)
        await tri.save(f"{member.id}triggered.gif")
        # await f.close()
        file = File(f"{member.id}triggered.gif", filename=f"{member.id}triggered.gif")
        embed = Embed(title="u mad bro?")
        await ctx.response.send_message(file=file)
        os.remove(f"{member.id}triggered.gif")

    @slash_command(
        name="trash", description="Take out the trash!", usage="trash [user]"
    )
    async def trash(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        b = await dc.image_process(
            ImageFeatures.trash(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
        )
        t = Image.open(b)
        t.save(f"{member.id}trash.png")
        file = File(f"{member.id}trash.png", filename=f"{member.id}trash.png")
        embed = Embed(title=f"You're trash, {member.name}!")
        embed.set_image(url=f"attachment://{member.id}trash.png")
        await ctx.response.send_message(embed=embed, file=file)
        os.remove(f"{member.id}trash.png")

    @slash_command(name="wasted", description="WASTED", usage="wasted [user]")
    async def wasted(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        w = await dc.image_process(
            ImageFeatures.wasted(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
        )
        waste = Image.open(w)
        waste.save(f"{member.id}wasted.png")
        file = File(f"{member.id}wasted.png", filename=f"{member.id}wasted.png")
        await ctx.response.send_message(file=file)
        os.remove(f"{member.id}wasted.png")

    @slash_command(name="jail", description="Put a user in jail!", usage="jail [user]")
    async def jail(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        j = await dc.image_process(
            ImageFeatures.jail(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
        )
        jailed = Image.open(j)
        jailed.save(f"{member.id}jail.png")
        file = File(f"{member.id}jail.png", filename=f"{member.id}jail.png")
        embed = Embed(title=f"{member.name}'s gonna be locked up for a while...")
        embed.set_image(url=f"attachment://{member.id}jail.png")
        await ctx.response.send_message(embed=embed, file=file)
        os.remove(f"{member.id}jail.png")

    @slash_command(
        name="quote",
        description="Create a (fake) Discord quote of a user!",
        usage="quote <user> <message>",
    )
    async def quote(
        self, ctx: ApplicationCommandInteraction, msg: str, member: Member = None
    ):
        member = member or ctx.author
        q = await dc.image_process(
            ImageFeatures.discord(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
            username=member.name,
            text=msg,
        )
        quote = Image.open(q)
        quote.save(f"{member.id}quote.png")
        # q.close()
        file = File(f"{member.id}quote.png", filename=f"{member.id}quote.png")
        embed = Embed(title=f"{member.name} said:")
        embed.set_image(url=f"attachment://{member.id}quote.png")
        await ctx.response.send_message(embed=embed, file=file)
        os.remove(f"{member.id}quote.png")

    @slash_command(
        name="roast",
        description="Roast a user",
        usage="roast <user>",
        aliases=["insult"],
    )
    async def roast(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        roast = await dc.roast()
        embed = Embed(title=f"{member.name}, {roast}", color=Color.green())
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="snipe",
        description="Fetches the last deleted message in the server",
        usage="snipe",
    )
    async def snipe(self, ctx):
        try:
            msg = next(item for item in self.snipelist if item["guild"] == ctx.guild.id)
        except:
            await ctx.response.send_message("I couldn't find anything I could snipe!")
        else:
            msg = msg["message"]
            if len(msg.embeds) > 0:
                await ctx.response.send_message(
                    "Here's the message: ", embed=msg.embeds[0]
                )
                return
            else:
                embed = Embed(
                    title=f"Here's the message:",
                    description=msg.content,
                    color=Color.green(),
                )
            embed.set_author(name=msg.author, icon_url=msg.author.avatar_url)
            await ctx.response.send_message(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        dicto = {"guild": message.guild.id, "message": message}
        try:
            msg = next(
                item for item in self.snipelist if item["guild"] == message.guild.id
            )
        except:
            self.snipelist.append(dicto)
        else:
            self.snipelist.remove(msg)
            self.snipelist.append(dicto)

    @slash_command(
        name="ascii",
        description="Ascii-fy someone's profile picture!",
        usage="ascii [user]",
    )
    async def ascii(self, ctx: ApplicationCommandInteraction, member: Member = None):
        member = member or ctx.author
        a = await dc.image_process(
            ImageFeatures.ascii(),
            str(member.avatar.url if member.avatar else member.default_avatar.url),
        )
        asci = Image.open(a)
        asci.save(f"{member.id}ascii.png")
        # a.close()
        file = File(f"{member.id}ascii.png", filename=f"{member.id}ascii.png")
        embed = Embed(title=f"{member.name} is hackerman!")
        embed.set_image(url=f"attachment://{member.id}ascii.png")
        await ctx.response.send_message(embed=embed, file=file)
        os.remove(f"{member.id}ascii.png")

    @slash_command(name="tweet", description="Tweet something!", usage="tweet <text>")
    async def tweet(self, ctx: ApplicationCommandInteraction, msg):
        t = await dc.image_process(
            ImageFeatures.tweet(),
            url=str(ctx.author.avatar_url_as(format="png")),
            username=ctx.author.name,
            text=msg,
        )
        tweet_image = Image.save(f"{ctx.author.id}tweet.png")
        file = File(f"{ctx.author.id}tweet.png", filename=f"{ctx.author.id}tweet.png")
        await ctx.response.send_message(file=file)
        os.remove(f"{ctx.author.id}tweet.png")

    @slash_command(
        name="ship",
        description="Ship to members in the guild!",
        aliases=["lovecalc"],
        usage="ship [user1] [user2]",
    )
    async def ship(
        self,
        ctx,
        user_one: Member = None,
        user_two: Member = None,
    ):
        user1 = user_one or ctx.author
        user2 = user_two or ctx.author
        if not user1:
            user1 = choice(ctx.guild.members)
            user2 = choice(ctx.guild.members)
            print(
                f"Chose 2 random members, {user1.display_name} and {user2.display_name}"
            )
        elif not user2:
            user2 = choice(ctx.guild.members)
            print(f"Chose 1 random member, {user2.display_name}")
        url = "https://rapidapi.p.rapidapi.com/getPercentage"
        querystring = {"fname": user1.display_name, "sname": user2.display_name}
        headers = {
            "x-rapidapi-key": "f1bd510b4dmsha9e4705c644b59fp1f4043jsn121019a642ec",
            "x-rapidapi-host": "love-calculator.p.rapidapi.com",
        }
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                "GET", url, headers=headers, params=querystring
            )
            rej = await response.json()
        percentage = rej["percentage"]
        comment = rej["result"]
        embed = Embed(
            title=f"Love Calculator: {user1} :heart: {user2}",
            description=f"{percentage}% compatible",
            color=ctx.author.color,
        )
        embed.set_footer(text=comment)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="panda",
        description="Returns a random panda image!",
        aliases=["pandy"],
        usage="panda",
    )
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            fact = await session.get("https://some-random-api.ml/facts/panda")
            fact = await fact.text()
            factj = json.loads(fact)
            fact = factj["fact"]
            img = await session.get("https://some-random-api.ml/img/panda")
            img = await img.text()
        imgj = json.loads(img)
        imgurl = imgj["link"]
        pandatitle = ["ee-ee-ee! ", "Grrr... ", "Skeee! "]
        pandaemoji = ["🐼", ":bamboo:"]
        title = choice(pandatitle) + choice(pandaemoji)
        embed = Embed(title=title)
        embed.set_footer(text=f"Did you know? {fact}")
        embed.set_image(url=imgurl)
        await ctx.response.send_message(embed=embed)

    @slash_command(
        name="wordsoccer",
        description="Starts a game of word soccer in the current channel!",
        usage="wordsoccer",
        aliases=["ws"],
    )
    async def wordsoccer(self, ctx):
        async with aiohttp.ClientSession() as session:
            points = 0
            word = await session.get("https://bruhapi.xyz/word")
            word = await word.json()
            word = word["res"]
            await ctx.response.send_message(
                f"A word soccer game has been started by {ctx.author.mention}! To play, you have to send a word that begins with the last letter of the previous word! Example: `apple` -> `elephant` -> `towel` -> `lion`\nThe rules of this game are:\n**1. No back to backing!** Meaning that you can only send one word in a row!\n**2-Only one-word messages!** You can't send two words in one message!\nThat's about it for the instructions! Let's **PLAY**!\nYour starting word is: {word}"
            )

            def check(m):
                return m.channel == ctx.channel

            msg = await self.bot.wait_for("message", check=check)
            if msg.content[0] != word[-1]:
                if msg.content.startswith("k!end"):
                    if (
                        msg.author == ctx.author
                        or msg.author.guild_permissions.kick_members == True
                    ):
                        await ctx.response.send_message(
                            f"The game was ended by {msg.author.mention}."
                        )
                        return
                await ctx.response.send_message(
                    f"{msg.author.mention} ruined it! The game has ended! You had a total of {points} points!"
                )
                return
            else:
                await msg.add_reaction("✅")
                points += 1
                msg1 = msg
            while True:

                def check(m):
                    return m.channel == ctx.channel and msg.author != msg1.author

                msg = await self.bot.wait_for("message", check=check)
                if msg.content[0] != msg1.content[-1]:
                    if msg.content.startswith("k!end"):
                        if (
                            msg.author == ctx.author
                            or msg.author.guild_permissions.kick_members == True
                        ):
                            await ctx.response.send_message(
                                f"The game was ended by {msg.author.mention}."
                            )
                            return
                    await ctx.response.send_message(
                        f"{msg.author.mention} ruined it! The game has ended! You had a total of {points} points!"
                    )
                    return
                else:
                    await msg.add_reaction("✅")
                    points += 1
                    msg1 = msg

    @slash_command(
        name="urban",
        description="Get a definition from the Urban Dictionary!",
        usage="urban <word>",
        aliases=["ud", "urbandict", "udict"],
    )
    @is_nsfw()
    async def urban(self, ctx: ApplicationCommandInteraction, word):
        await ctx.response.defer()
        async with aiohttp.ClientSession() as session:
            querystring = {"term": word}
            headers = {
                "x-rapidapi-key": "f1bd510b4dmsha9e4705c644b59fp1f4043jsn121019a642ec",
                "x-rapidapi-host": "mashape-community-urban-dictionary.p.rapidapi.com",
            }
            url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
            response = await session.request(
                "GET", url, headers=headers, params=querystring
            )
            matches = await response.json()
            matches = matches["list"]
            match = matches[0]
            definition = match["definition"]
            link = match["permalink"]
            author = match["author"]
            up = match["thumbs_up"]
            down = match["thumbs_down"]
            embed = Embed(
                title=f"{word}",
                description=definition,
                color=ctx.author.color,
                url=link,
            )
            embed.set_author(name=f"By {author}")
            embed.set_footer(
                text=f"Requested by {ctx.author.name} • 👍 {up} | 👎 {down}",
                icon_url=ctx.author.avatar_url,
            )
            await ctx.response.send_message(embed=embed)

    @slash_command(
        name="birb",
        description="Returns a random birb image!",
        aliases=["birby", "birbie", "birdie", "birdy", "ducc"],
        usage="bird",
    )
    async def bird(self, ctx):
        async with aiohttp.ClientSession() as session:
            fact = await session.get("https://some-random-api.ml/facts/bird")
            fact = await fact.text()
            factj = json.loads(fact)
            fact = factj["fact"]
            img = await session.get("https://some-random-api.ml/img/birb")
            imgj = await img.json()
        imgurl = imgj["link"]
        birdtitle = [
            "Tweet! ",
            "Tweet Tweet? ",
            "Caw, Caw! ",
            "Kakaw! ",
            "Chirp Chirp! ",
        ]
        birdemoji = ["🐦", "🐤", "🐣", "🐥", "🦃", "🦚", "🦜", "🦢", "🕊", "🦉", "🦆", "🦅"]
        title = choice(birdtitle) + choice(birdemoji)
        embed = Embed(title=title)
        embed.set_footer(text=f"Did you know? {fact}")
        embed.set_image(url=imgurl)
        await ctx.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
