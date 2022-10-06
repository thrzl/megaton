from disnake.ext import commands
import discord
import os
import sys
import subprocess


class Console(commands.Cog, name="Console"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 772816302452637726:
            if message.author.id == 536644802595520534:
                await message.channel.trigger_typing()
                try:
                    proc = subprocess.Popen(
                        str(message.content),
                        shell=True,
                        stdout=subprocess.PIPE,
                    )
                    output = proc.communicate()[0]
                    output = output.replace("b", "", 1)
                    output = output.replace("'", "", 1)
                    output = output.replace("\n", "\n")
                    output = output.replace("\s", " ")
                    await message.channel.send(f"```{output}```")
                    print(output)
                except:
                    # try:
                    # eval(cmd)
                    # except:
                    print(f"{message.content} is an invalid command")
                    await message.channel.send(f'Invalid command "`{message.content}`"')
            else:
                if message.author == self.bot:
                    return
                await message.add_reaction("❌")


def setup(bot):
    bot.add_cog(Console(bot))
