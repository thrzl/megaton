from datetime import timedelta
from random import choice
from sqlite3 import TimestampFromTicks
from disnake.errors import HTTPException, Forbidden
from disnake.ext import commands
from disnake.ext.commands import slash_command
from disnake import Color, Member, Object
from disnake.ext.commands.slash_core import ApplicationCommandInteraction
import asyncio
from disnake.ext.commands.cooldowns import BucketType
import ksoftapi
from bot import Megaton, HeirarchyErrorType, HeirarchyError, Embed
from disnake.utils import get
from typing import List, Optional
from os import environ
from utils.data import Moderation as _mod

kclient = ksoftapi.Client(environ.get("KSOFT_KEY"))


def has_voted():
    async def predicate(ctx):
        # if not await ctx.bot.dbl.get_user_vote(ctx.author.id):
        #     embed=Embed(title="That's a voter-only command!",description="You can't use this command without voting! Use the `vote` command to vote for me and unlock this command!",color=Color.blue())
        #     await ctx.send(embed=embed)
        # return await ctx.bot.dbl.get_user_vote(ctx.author.id)
        return True

    return commands.check(predicate)


class Moderation(commands.Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
        # self.dbl = bot.dbl

    def assert_heirarchy(
        self, ctx: ApplicationCommandInteraction, member: Member
    ) -> bool:
        """checks if the bot and user have the correct permissions to complete the action

        Parameters
        ----------
        ctx : ApplicationCommandInteraction
            the interaction context
        member : Member
            the 'victim' of the action

        Returns
        -------
        bool
            returns true if the bot and user have the correct permissions

        Raises
        ------
        HeirarchyError
            the bot or user does not have the correct permissions
        """
        if ctx.guild.owner_id == ctx.author.id:
            return True
        if ctx.guild.owner_id == member.id:
            return False
        if member.top_role >= ctx.author.top_role:
            raise HeirarchyError(
                text=f"{member.name}'s highest role is above yours, so you can't complete this action."
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            raise HeirarchyError(
                text=f"{member.name}'s highest role is above mine, so i can't complete this action. ask the server owner to move my role above {member.name}'s highest role."
            )
        return True

    @slash_command(
        name="scan",
        description="Checks your member list against the KSoft.Si bans list.",
        usage="scan [options]",
    )
    @commands.has_permissions(manage_guild=True, ban_members=True)
    @commands.bot_has_permissions(ban_members=True, kick_members=True)
    @commands.max_concurrency(1, per=BucketType.default, wait=True)
    @has_voted()
    async def scan(self, ctx: ApplicationCommandInteraction, *args):
        ulist: List[Member] = []
        await ctx.response.send_message(
            f"Beginning Scan... Estimated Duration: {len(ctx.guild.members)*3} seconds"
        )
        for member in ctx.guild.members:
            if not member.bot:
                if await kclient.bans.check(member.id):
                    ban = await kclient.bans.info(member.id)
                    ulist.append(member)
                    if "-ban" in args or "-b" in args:
                        await ctx.guild.ban(
                            member,
                            reason=f"Banned by {ctx.author} through scan command.",
                            delete_message_days=0,
                        )
                        await asyncio.sleep(5)
                        break
                    elif "-kick" in args or "-k" in args:
                        await ctx.guild.kick(
                            member,
                            reason=f"Kicked by {ctx.author} through scan command.",
                        )
                await asyncio.sleep(3)
        await ctx.send("Scan complete!")

    @scan.error
    async def on_error(self, ctx: ApplicationCommandInteraction, e):
        if isinstance(e, commands.MaxConcurrencyReached):
            embed = Embed(
                title="this command is currently being used by someone else!",
                description="we'll run the command when it's ready, and notify you when the command is running!",
                color=Color.green(),
            )
            await ctx.send(embed=embed)
            ctx.from_concurrency = True

    @slash_command(
        name="lock",
        description="Locks the channel for a specified amount of time.",
        aliases=["lockdown", "close"],
        usage="lock",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lock(
        self,
        ctx: ApplicationCommandInteraction,
        time: str = commands.Param(autocomplete=_mod.times, default=None),
        reason="No Reason Provided.",
    ):
        """

        Parameters
        ----------
        ctx : ApplicationCommandInteraction
            the interaction context
        time : str, optional
            the amount of time to lock the channel for
        reason : str, optional
            the reason the member was timed out, by default "No Reason Provided."
        """
        if not time:
            seconds, time = self.bot.calculate_time(time)
        else:
            formatendtime = "further notice"
        embed = Embed(
            title="this channel was locked 🔒",
            description=f"this channel was locked down for reason: {reason}",
            color=Color.red(),
        )
        embed.set_footer(
            text=f"this channel is locked until {formatendtime} ● responsible moderator: {ctx.author.name}"
        )
        msg = await ctx.send(embed=embed)
        guildroles = await ctx.guild.fetch_roles()
        everyone = get(guildroles, name="@everyone")
        await ctx.channel.set_permissions(
            everyone, send_messages=False, read_messages=True
        )
        if time:
            await asyncio.sleep(seconds)
            embed = Embed(
                title="this channel is now unlocked 🔓",
                description=f"this channel is now unlocked.",
                color=Color.blue(),
            )
            embed.set_footer(text=f"this channel was unlocked at {formatendtime}.")
            await ctx.channel.set_permissions(everyone, overwrite=None)
            await msg.edit(embed=embed)

    @slash_command(
        name="unlock",
        description="Unlocks a channel, making it so that members can type again.",
        aliases=["unlockdown", "open"],
        usage="unlock",
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        guildroles = await ctx.guild.fetch_roles()
        everyone = get(guildroles, name="@everyone")
        await ctx.channel.set_permissions(everyone, overwrite=None)
        embed = Embed(
            title="This channel was unlocked",
            description=f"This channel is now unlocked.",
        )
        await ctx.send(embed=embed)

    @slash_command(
        name="clean",
        description="cleans x messages in a channel.",
        aliases=["c", "wipe"],
        usage="clean <number>",
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clean(
        self,
        ctx: ApplicationCommandInteraction,
        amount=2,
        member: Optional[Member] = None,
    ):
        check = lambda m: m.author == member if member else lambda m: True
        await ctx.channel.purge(limit=amount + 1, bulk=True, check=check)
        delmsg = await ctx.channel.send(
            embed=Embed(
                description=f"just cleaned up **{amount}** messages. this message will be deleted in 3 seconds."
            ).set_author(name=choice(_mod.clean_msgs))
        )
        await asyncio.sleep(3)
        await delmsg.delete()

    @slash_command(
        name="kick", description="kicks a user", aliases=["k"], usage="kick <user>"
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        reason="No reason provided",
    ):
        if (
            member.top_role >= ctx.author.top_role
            and ctx.guild.owner_id != ctx.author.id
        ):
            await ctx.send(
                embed=Embed(
                    description=f"{member.name}'s highest role is above yours, so you can't complete this action."
                )
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above mine, I've been H E I R A R C H Y ' D"
            )
        else:
            try:
                await member.send(
                    f"You have been kicked from {ctx.guild.name} for: \n" + reason
                )
            except:
                await ctx.send("The member has their DMs closed. I still will kick...")
            await member.kick(reason=reason)
            await ctx.send(str(member) + " just got the boot. :boot: :sunglasses:")

    @slash_command(
        name="warn", description="Warns a user", aliases=["w"], usage="warn user>"
    )
    @commands.has_permissions(kick_members=True)
    async def warn(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        reason="No reason provided",
    ):
        if type(member) == Member:
            c = self.bot.check_heirarchy(ctx, member)
            if c == HeirarchyErrorType.NO_PERMISSION:
                return await ctx.send(
                    f"whoops... {member.name}'s highest role is above yours, you can't complete this action"
                )
            elif c == HeirarchyErrorType.SELF_NO_PERMISSION:
                return await ctx.send(
                    f"whoops... {member.name}'s highest role is above mine, i can't complete this action. maybe try talking to the server owner?"
                )
        else:
            try:
                await member.send(
                    f"you've been warned in {ctx.guild.name} for: {reason}"
                )
            except:
                await ctx.response.send_message("the member has their DMs closed.")

    @slash_command(
        name="ban", description="Bans a user", aliases=["b"], usage="ban <user>"
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        reason="no reason provided",
    ):
        c = self.bot.check_heirarchy(ctx.author, member)
        if c == HeirarchyErrorType.NO_PERMISSION:
            return await ctx.send(
                f"whoops... {member.name}'s highest role is above yours, you can't complete this action"
            )
        elif c == HeirarchyErrorType.SELF_NO_PERMISSION:
            return await ctx.send(
                f"whoops... {member.name}'s highest role is above mine, i can't complete this action. maybe try talking to the server owner?"
            )
        else:
            try:
                user = await self.bot.fetch_user(member.id)
                await user.send(
                    f"the **ban hammer** has spoken to you in {ctx.guild.name} with reason: {reason}"
                )
            except:
                await ctx.guild.ban(member, reason=reason)

    @slash_command(
        name="unban", description="Unbans a user", aliases=["ub"], usage="unban <user>"
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx: ApplicationCommandInteraction, member: Object):
        try:
            user = await self.bot.fetch_user(member.id)
        except:
            user = None
        try:
            await ctx.guild.unban(member)
        except:
            await ctx.send(
                f"{user.name} doesn't appear to be banned."
            ) if not user else await ctx.send(
                f"{member.id} doesn't appear to be banned."
            )
        try:
            user.send("You have been unbanned from " + ctx.guild.name)
        except (HTTPException, Forbidden):
            pass
        await ctx.send(user + " has been unbanned from " + ctx.guild.name)

    @slash_command(
        name="timeout",
        description="Mutes a user. In other words, removes their ability to chat.",
        aliases=["m"],
        usage="timeout <user>",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def timeout(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        time: str = commands.Param(autocomplete=_mod.times),
        reason="No reason provided",
    ):
        """

        Parameters
        ----------
        ctx : ApplicationCommandInteraction
            the interaction context
        member : Member
            the member to time out
        time : str, optional
            the amount of time to time the user out for
        reason : str, optional
            the reason the user was timed out, by default "No reason provided"
        """
        if (
            member.top_role >= ctx.author.top_role
            and ctx.guild.owner_id != ctx.author.id
        ):
            await ctx.send(
                f"**uhm...** {member.name}'s highest role is above yours, you've been H E I R A R C H Y ' D"
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above mine, I've been H E I R A R C H Y ' D"
            )
        else:
            try:
                await member.send(
                    "You have been muted in " + ctx.guild.name + "\nReason: " + reason
                )
            except:
                await ctx.send("User's DMs are closed. Still muting...")
            if time:
                duration, end = self.bot.calculate_time(time)
                await member.timeout(
                    duration=duration, reason=f"muted by {ctx.author}: {reason}"
                )
                timestamp = end.strftime("%s")
                await ctx.send(
                    embed=Embed(
                        description=f"{member} has been timed out until <t:{timestamp}:f>."
                    ).set_author(name="member muted")
                )
            else:
                await member.timeout(
                    until=None, reason=f"muted by {ctx.author}: {reason}"
                )
                await ctx.send(
                    embed=Embed(
                        description=f"{member} has been timed out indefinitely."
                    ).set_author(name="member muted")
                )

    @slash_command(
        name="lockout",
        description="Locks a user out of a channel. In other words, removes their ability to see a given channel.",
        aliases=["cb"],
        usage="lockout <user>",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockout(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        reason="No reason provided",
    ):
        if (
            member.top_role >= ctx.author.top_role
            and ctx.guild.owner_id != ctx.author.id
        ):
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above yours, you've been H E I R A R C H Y ' D"
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above mine, I've been H E I R A R C H Y ' D"
            )
        else:
            try:
                await member.send(
                    f"You have been locked out of {ctx.channel.name} in {ctx.guild.name}\nReason: {reason}"
                )
            except:
                pass
            await ctx.channel.set_permissions(
                member, send_messages=False, read_messages=False
            )
            await ctx.send(str(member) + " has been locked out of this channel..")

    @slash_command(
        name="unlockout",
        description="Unlocks a user out of a channel. In other words, removes their ability to see a given channel.",
        aliases=["ucb"],
        usage="unlockout <user>",
    )
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlockout(self, ctx: ApplicationCommandInteraction, member: Member):
        if (
            member.top_role >= ctx.author.top_role
            and ctx.guild.owner_id != ctx.author.id
        ):
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above yours, you've been H E I R A R C H Y ' D"
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above mine, I've been H E I R A R C H Y ' D"
            )
        else:
            try:
                await member.send(
                    f"You have been un-locked out of {ctx.channel.name} in {ctx.guild.name}."
                )
            except:
                pass
            await ctx.channel.set_permissions(member, overwrite=None)
            await ctx.send(str(member) + " has been unlocked from this channel..")

    @slash_command(
        name="untimeout",
        description="untimeouts a user. In other words, gives them  their ability to chat back.",
        aliases=["sum", "sumute"],
        usage="untimeout <user>",
    )  # still in testing...
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def untimeout(
        self,
        ctx: ApplicationCommandInteraction,
        member: Member,
        reason="No reason provided",
    ):
        if (
            member.top_role >= ctx.author.top_role
            and ctx.guild.owner_id != ctx.author.id
        ):
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above yours, you've been H E I R A R C H Y ' D"
            )
        if member.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send(
                f"**Erhm...** {member.name}'s highest role is above mine, I've been H E I R A R C H Y ' D"
            )
        else:
            try:
                await member.send(
                    "You have been unmuted in " + ctx.guild.name + "\nReason: " + reason
                )
            except:
                await ctx.send("User's DMs are closed. Still unmuting...")
            for channel in ctx.guild.channels:
                try:
                    await channel.set_permissions(member, overwrite=None)
                except:
                    # await ctx.send("I was unable to mute.")
                    ctx.author.send(f"I was unable to unmute in {channel.mention}.")
                    return
            await ctx.send(str(member) + " has been unmuted.")


def setup(bot):
    bot.add_cog(Moderation(bot))
