from disnake.ext import commands
import discord
import difflib
from disnake.ext import buttons
from pymongo import MongoClient
from disnake.ext.forms import ReactionMenu
from dpymenus import Page, PaginatedMenu


hidden = ["Help", "Error", "Welcome", "stat", "Bot Owner", "Jishaku", "TopGG"]


class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(
            f"<@!{self.bot.user.id}>"
        ) and message.content.endswith(f"<@!{self.bot.user.id}>"):
            p = await get_prefix(message)
            embed = Embed(
                title="Hey there! 👋🏽",
                description=f"I couldn't help but notice you mentioned me! My prefix for this server is `{p}`, but you can always just mention me to use commands!",
                color=discord.Color.green(),
            )
            await message.channel.send(embed=embed)

    @commands.command(name="pagetest")
    async def pagetest(self, ctx):
        ccmds = {}
        helpdict = []
        # clist = []
        for c in self.bot.cogs.values():
            ccmds[c.qualified_name] = []
            clist = ccmds[c.qualified_name]
            if c.qualified_name not in hidden:
                cogname = c.qualified_name.replace("_", " ")

                embed = Embed(color=discord.Color.green())
                cmds = c.get_commands()

                for d in cmds:
                    clist.append(f"k!{d.name.lower()}")
                clist = str(clist).replace("[", "")
                clist = clist.replace("]", "")
                clist = clist.replace("'", "`")
                embed.add_field(
                    name=c.qualified_name.replace("_", " "), value=clist, inline=False
                )

                helpdict.append(embed)
                # helpdict.append()
            continue
        print(helpdict)
        menu = PaginatedMenu(ctx)
        menu.allow_multisession()
        menu.show_page_numbers()
        menu.add_pages(helpdict)
        menu.show_command_message()
        await menu.open()

    @commands.command(name="helpbutwithoutpermsforproperpagination")
    async def helpnomanage(self, ctx: ApplicationCommandInteraction, command="none"):
        p = await get_prefix(ctx)
        if command == "none":
            embed = Embed(
                title="megaton Help",
                description=f"**⚠ I do not have the `MANAGE_MESSAGES` permission in this server. Many features are reliant on this, so please give me this ability! ⚠**\nMy prefix for this server: `{p}`\n`<arg>` is required\n`[arg]` is optional",
                color=discord.Color.green(),
            )
            # embed.add_field(name=f"News 📰",value=f"Use `{p}config` to set up custom options for your server!",inline=False)
            for c in self.bot.cogs.values():
                clist = []
                if c.qualified_name in hidden:
                    pass
                else:
                    cmds = c.get_commands()
                    for d in cmds:
                        clist.append(f"{p}{d.name.lower()}")
                    clist = str(clist).replace("[", "")
                    clist = clist.replace("]", "")
                    clist = clist.replace("'", "`")
                    embed.add_field(
                        name=c.qualified_name.replace("_", " "),
                        value=clist,
                        inline=False,
                    )
            embed.add_field(
                name=f"Links",
                value=f"[Support Server](https://discord.gg/bNtj2nFnYA) | [Invite Me](https://discord.com/api/oauth2/authorize?client_id=766818911505088514&permissions=268823622&scope=bot) | [Vote for Me](https://top.gg/bot/766818911505088514)",
                inline=False,
            )
            embed.set_footer(
                text=f"Type '{p}help <category | command>' to get help with different commands!"
            )
            await ctx.send(embed=embed)
        elif command.lower().startswith("mod"):
            embed = Embed(
                title="Moderation Help",
                description="Help with moderation commands",
                color=ctx.author.color,
            )
            for c in self.bot.cogs.values():
                if c.qualified_name == "Moderation":
                    mcog = c
            for cmd in mcog.get_commands():
                embed.add_field(
                    name=f"{p}{cmd.name}",
                    value=f"{cmd.description}\nUsage: ```{p}{cmd.usage}```",
                )
            await ctx.send(embed=embed)
        elif command.lower().startswith("bot"):
            embed = Embed(
                title="Bot Info Help",
                description="Help with my Bot Information commands!",
                color=ctx.author.color,
            )
            cog = self.bot.get_cog("Bot_Info")
            for i in cog.get_commands():
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            await ctx.send(embed=embed)
        elif command.lower().startswith("util"):
            embed = Embed(
                title="Utility Help",
                description="Help with utility commands",
                color=ctx.author.color,
            )
            cog = self.bot.get_cog("Utility")
            for i in cog.get_commands():
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            await ctx.send(embed=embed)
        elif command.lower().startswith("econ"):
            embed = Embed(
                title="Economy Help",
                description="Help with my Economy system!",
                color=ctx.author.color,
            )
            cog = self.bot.get_cog("Economy")
            for i in cog.get_commands():
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            await ctx.send(embed=embed)
        elif command.lower().startswith("fun"):
            embed = Embed(
                title="Fun Help",
                description="Help with fun commands",
                color=ctx.author.color,
            )
            cog = self.bot.get_cog("Fun")
            for i in cog.get_commands():
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            await ctx.send(embed=embed)
        else:
            cmdn = []
            close = ""
            for i in self.bot.commands:
                if i.name.lower() == command.lower() or command.lower() in i.aliases:
                    cmdn.append(i.name.lower())
                    embed = Embed(title=f"{i.name}", color=discord.Color.green())
                    if i.description == "":
                        description = "None"
                    else:
                        description = i.description
                    if i.usage == "":
                        usage = "None"
                    else:
                        usage = i.usage
                        usage = f"{p}{usage}"
                    embed.add_field(name="Description", value=description, inline=False)
                    embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
                    await ctx.send(embed=embed)
                    return
            if command.lower() not in cmdn:
                for i in self.bot.commands:
                    if difflib.SequenceMatcher(None, command, i.name).ratio() > 0.5:
                        close = close + f"`{i.name}`\n"
            if len(close) < 1:
                for i in self.bot.commands:
                    for a in i.aliases:
                        if difflib.SequenceMatcher(None, command, a).ratio() > 0.5:
                            close = close + f"`{i.name}` \n"
            if len(close) > 0:
                close = str(close).replace("[", "")
                close = close.replace("]", "")
                close = close.replace("'", "")
                close = close.replace(",", "")
                embed = Embed(
                    title="Command not found...",
                    description=f"Did you mean:\n {close}",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("I couldn't find that command.")

    @commands.command(
        name="Help", description="Opens the help menu!", usage="help [command]"
    )
    async def help(self, ctx: ApplicationCommandInteraction, command="none"):
        helpcog = self.bot.get_cog("Help")
        if not ctx.guild.me.permissions_in(ctx.channel).manage_messages:
            await helpcog.helpnomanage(ctx, command)
        else:
            await helpcog.helpwithperms(ctx, command)

    @commands.command(
        name="Helpbutwithpagination",
        description="Opens the help menu!",
        usage="help [command]",
    )
    async def helpwithperms(self, ctx: ApplicationCommandInteraction, command="none"):
        p = await get_prefix(ctx)
        elist = []
        if command == "none":
            embed = Embed(
                title="megaton Help",
                description=f"My prefix for this server: `{p}`\n`<arg>` is required\n`[arg]` is optional",
                color=discord.Color.green(),
            )
            ccmds = {}
            helpdict = []
            # clist = []
            for c in self.bot.cogs.values():
                ccmds[c.qualified_name] = []
                clist = ccmds[c.qualified_name]
                if c.qualified_name not in hidden and c.get_commands():
                    cogname = c.qualified_name.replace("_", " ")

                    embed = Embed(title="megaton Help", color=discord.Color.green())
                    cmds = c.get_commands()

                    for d in cmds:
                        clist.append(f"k!{d.name.lower()}")
                    clist = str(clist).replace("[", "")
                    clist = clist.replace("]", "")
                    clist = clist.replace("'", "`")
                    embed.add_field(
                        name=c.qualified_name.replace("_", " "),
                        value=clist,
                        inline=False,
                    )
                    embed.add_field(
                        name=f"Links",
                        value=f"[Support Server](https://discord.gg/bNtj2nFnYA) | [Invite Me](https://discord.com/api/oauth2/authorize?client_id=766818911505088514&permissions=268823622&scope=bot) | [Vote for Me](https://top.gg/bot/766818911505088514)",
                        inline=False,
                    )
                    embed.set_footer(
                        text=f"Type '{p}help <category | command>' to get help with different commands!"
                    )
                    helpdict.append(embed)
                    # helpdict.append()
                continue
            menu = ReactionMenu(ctx, helpdict)
            await menu.start()
            print("Opened menu")
        #    """
        elif command.lower().startswith("mod"):
            embed = Embed(
                title="Moderation Help",
                description="Help with moderation commands",
                color=discord.Color.green(),
            )
            for c in self.bot.cogs.values():
                if c.qualified_name == "Moderation":
                    mcog = c
            for cmd in mcog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Moderation Help",
                        description="Help with moderation commands",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{cmd.name}",
                    value=f"{cmd.description}\nUsage: ```{p}{cmd.usage}```",
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            menu = PaginatedMenu(ctx).add_pages(elist)
            menu.show_page_numbers()
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                menu.allow_multisession()
            else:
                menu.show_command_message()
                await ctx.send(
                    "I'm missing the `Manage Messages` permission, so this may not work as intended."
                )
            await menu.open()

        elif command.lower().startswith("bot"):
            embed = Embed(
                title="Bot Info Help",
                description="Help with my Bot Information commands!",
                color=discord.Color.green(),
            )
            cog = self.bot.get_cog("Bot_Info")
            for i in cog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Bot Info Help",
                        description="Help with my Bot Information commands!",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            menu = PaginatedMenu(ctx).add_pages(elist)
            menu.show_page_numbers()
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                menu.allow_multisession()
            else:
                menu.show_command_message()
                await ctx.send(
                    "I'm missing the `Manage Messages` permission, so this may not work as intended."
                )
            await menu.open()

        elif command.lower().startswith("util"):
            embed = Embed(
                title="Utility Help",
                description="Help with utility commands",
                color=discord.Color.green(),
            )
            cog = self.bot.get_cog("Utility")
            for i in cog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Utility Help",
                        description="Help with utility commands",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            menu = PaginatedMenu(ctx).add_pages(elist)
            menu.show_page_numbers()
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                menu.allow_multisession()
            else:
                menu.show_command_message()
                await ctx.send(
                    "I'm missing the `Manage Messages` permission, so this may not work as intended."
                )
            await menu.open()

        elif command.lower().startswith("econ"):
            embed = Embed(
                title="Economy Help",
                description="Help with my Economy system!",
                color=discord.Color.green(),
            )
            cog = self.bot.get_cog("Economy")
            for i in cog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Economy Help",
                        description="Help with my Economy system!",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            menu = PaginatedMenu(ctx).add_pages(elist)
            menu.show_page_numbers()
            if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                menu.allow_multisession()
            else:
                menu.show_command_message()
                await ctx.send(
                    "I'm missing the `Manage Messages` permission, so this may not work as intended. For example, to open a new menu you must close the old one first."
                )
            await menu.open()

        elif command.lower().startswith("fun"):
            embed = Embed(
                title="Fun Help",
                description="Help with fun commands",
                color=discord.Color.green(),
            )
            cog = self.bot.get_cog("Fun")
            for i in cog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Fun Help",
                        description="Help with fun commands",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            else:
                menu = PaginatedMenu(ctx)
                menu.show_page_numbers()
                menu.add_pages(elist)
                if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                    menu.allow_multisession()
                else:
                    menu.show_command_message()
                    await ctx.send(
                        "I'm missing the `Manage Messages` permission, so this may not work as intended."
                    )
                await menu.open()

        elif command.lower().startswith("music"):
            embed = Embed(
                title="Music Help",
                description="Help with music commands",
                color=discord.Color.green(),
            )
            cog = self.bot.get_cog("Music")
            for i in cog.get_commands():
                if len(embed.fields) >= 5:
                    elist.append(embed)
                    embed = Embed(
                        title="Music Help",
                        description="Help with music commands",
                        color=discord.Color.green(),
                    )
                embed.add_field(
                    name=f"{p}{i.name}",
                    value=f"{i.description}\nUsage: ```{p}{i.usage}```",
                    inline=True,
                )
            if len(elist) < 2:
                return await ctx.send(embed=elist[0])
            else:
                menu = PaginatedMenu(ctx)
                menu.show_page_numbers()
                menu.add_pages(elist)
                if ctx.guild.me.permissions_in(ctx.channel).manage_messages:
                    menu.allow_multisession()
                else:
                    menu.show_command_message()
                    await ctx.send(
                        "I'm missing the `Manage Messages` permission, so this may not work as intended."
                    )
                await menu.open()
            # """
        else:
            cmdn = []
            close = ""
            for i in self.bot.commands:
                if i.name.lower() == command.lower() or command.lower() in i.aliases:
                    cmdn.append(i.name.lower())
                    embed = Embed(title=f"{i.name}", color=discord.Color.green())
                    if i.description == "":
                        description = "None"
                    else:
                        description = i.description
                    if i.usage == "":
                        usage = "None"
                    else:
                        usage = i.usage
                        usage = f"{p}{usage}"
                    embed.add_field(name="Description", value=description, inline=False)
                    embed.add_field(name="Usage", value=f"```{usage}```", inline=False)
                    await ctx.send(embed=embed)
                    return
            if command.lower() not in cmdn:
                for i in self.bot.commands:
                    if difflib.SequenceMatcher(None, command, i.name).ratio() > 0.5:
                        close = close + f"`{i.name}`\n"
            if len(close) < 1:
                for i in self.bot.commands:
                    for a in i.aliases:
                        if difflib.SequenceMatcher(None, command, a).ratio() > 0.5:
                            close = close + f"`{i.name}` \n"
            if len(close) > 0:
                close = str(close).replace("[", "")
                close = close.replace("]", "")
                close = close.replace("'", "")
                close = close.replace(",", "")
                embed = Embed(
                    title="Command not found...",
                    description=f"Did you mean:\n {close}",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("I couldn't find that command.")


def setup(bot):
    bot.add_cog(Help(bot))
