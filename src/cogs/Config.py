from __future__ import annotations
from typing import Optional
from disnake import ui, components
from disnake.ext import commands
from disnake import (
    GuildCommandInteraction,
    MessageInteraction,
    Guild,
    TextChannel,
    ChannelType,
)

from src.bot import Embed, Megaton

from src.db import Database

from src.utils.emojis import (
    CHECK_EMOJI,
    CROSS_EMOJI,
    STAR_EMOJI,
    WRENCH_EMOJI,
    CHANNEL_EMOJI,
    WELCOME_EMOJI,
)


class ConfigSelect(ui.StringSelect[ui.View]):
    def __init__(
        self,
        db: Database,
        bot: Megaton,
        config_inter: GuildCommandInteraction,
    ):
        options = [
            components.SelectOption(label="leveling", emoji=STAR_EMOJI),
            components.SelectOption(label="welcome messages", emoji=WELCOME_EMOJI),
            components.SelectOption(label="exit", emoji=CROSS_EMOJI),
        ]
        super().__init__(
            placeholder="select a setting to configure",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="config_select",
        )
        self.db = db
        self.bot = bot
        self.config_inter = config_inter

    async def callback(self, interaction: MessageInteraction) -> None:
        selected = self.values[0]

        if selected == "exit":
            await interaction.delete_original_message()
            return

        guild = interaction.guild
        assert guild is not None

        if selected == "leveling":
            await interaction.response.defer()
            guild_settings = await self.db.get_guild_settings(guild.id)
            if guild_settings.leveling == 0:
                await guild_settings.update_leveling_channel(1)
                await interaction.followup.send(
                    embed=Embed(
                        description=f"{CHECK_EMOJI} enabled leveling in this guild!"
                    ),
                    ephemeral=True,
                )
            else:
                await guild_settings.update_leveling_channel(0)
                await interaction.followup.send(
                    embed=Embed(
                        description=f"{CROSS_EMOJI} disabled leveling in this guild!"
                    ),
                    ephemeral=True,
                )
            await self._refresh_config_embed(guild)
        elif selected == "welcome messages":
            welcome_view = WelcomeChannelView(
                db=self.db,
                bot=self.bot,
                guild=guild,
                author_id=interaction.author.id,
                config_inter=self.config_inter,
            )
            await interaction.response.send_message(
                embed=Embed(
                    title=f"{CHANNEL_EMOJI} welcome message setup",
                    description="select a text channel for welcome messages, or disable it below",
                ),
                view=welcome_view,
                ephemeral=True,
            )

    async def _refresh_config_embed(self, guild: Guild) -> None:
        settings = await self.db.get_guild_settings(guild.id)
        embed = Embed(title=f"{WRENCH_EMOJI} configuration options")
        if settings.leveling == 0:
            embed.add_field(name=f"{STAR_EMOJI} leveling system", value=CROSS_EMOJI)
        else:
            embed.add_field(name=f"{STAR_EMOJI} leveling system", value=CHECK_EMOJI)
        if settings.welcoming != 0:
            channel = guild.get_channel(int(settings.welcoming))
            assert channel is not None
            embed.add_field(
                name=f"{WELCOME_EMOJI} welcome messages", value=channel.mention
            )
        else:
            embed.add_field(name=f"{WELCOME_EMOJI} welcome messages", value=CROSS_EMOJI)
        await self.config_inter.edit_original_message(embed=embed)


class WelcomeChannelView(ui.View):
    def __init__(
        self,
        db: Database,
        bot: Megaton,
        guild: Guild,
        author_id: int,
        config_inter: GuildCommandInteraction,
    ):
        super().__init__()
        self.db = db
        self.bot = bot
        self.guild = guild
        self.author_id = author_id
        self.config_inter = config_inter

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.author.id != self.author_id:
            await interaction.response.send_message(
                "you are not allowed to interact with this menu", ephemeral=True
            )
            return False
        return True

    async def _refresh_config_embed(self, guild: Guild) -> None:
        settings = await self.db.get_guild_settings(guild.id)
        embed = Embed(title=f"{WRENCH_EMOJI} configuration options")
        if settings.leveling == 0:
            embed.add_field(name=f"{STAR_EMOJI} leveling system", value=CROSS_EMOJI)
        else:
            embed.add_field(name=f"{STAR_EMOJI} leveling system", value=CHECK_EMOJI)
        if settings.welcoming != 0:
            channel = guild.get_channel(int(settings.welcoming))
            assert channel is not None
            embed.add_field(
                name=f"{WELCOME_EMOJI} welcome messages", value=channel.mention
            )
        else:
            embed.add_field(name=f"{WELCOME_EMOJI} welcome messages", value=CROSS_EMOJI)
        await self.config_inter.edit_original_message(embed=embed)

    @ui.channel_select(
        custom_id="welcome_channel_select",
        placeholder="select your welcome channel",
        channel_types=[ChannelType.text],
        max_values=1,
    )
    async def welcome_channel_select(
        self, select: ui.ChannelSelect, interaction: MessageInteraction
    ):
        channel = select.values[0]
        assert isinstance(channel, TextChannel)
        guild = interaction.guild
        assert guild is not None
        guild_settings = await self.db.get_guild_settings(guild.id)
        await guild_settings.update_welcoming_channel(channel.id)
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=Embed(description=f"set the welcome channel to {channel.mention}!"),
            view=None,
        )
        await interaction.delete_original_message()
        self.stop()
        await self._refresh_config_embed(guild)

    @ui.button(
        label="disable",
        emoji=CROSS_EMOJI,
        custom_id="welcome_disable",
    )
    async def disable_button(self, _button: ui.Button, interaction: MessageInteraction):
        guild = interaction.guild
        assert guild is not None
        guild_settings = await self.db.get_guild_settings(guild.id)
        await guild_settings.update_welcoming_channel(0)
        await interaction.response.defer()
        await interaction.edit_original_message(
            embed=Embed(description="disabled welcoming in this guild!"),
            view=None,
        )
        await interaction.delete_original_message()
        self.stop()
        await self._refresh_config_embed(guild)


class ConfigView(ui.View):
    def __init__(
        self,
        author_id: int,
        db: Database,
        bot: Megaton,
        guild: Guild,
        config_inter: GuildCommandInteraction,
    ):
        super().__init__()
        self.author_id = author_id
        self.db = db
        self.bot = bot
        self.guild = guild
        self.add_item(ConfigSelect(db, bot, config_inter))

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        if interaction.author.id != self.author_id:
            await interaction.response.send_message(
                "you are not allowed to interact with this menu", ephemeral=True
            )
            return False
        return True


class Config(commands.Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
        if bot.db is None:
            raise ValueError("database connection is not established.")
        self.db = bot.db

    @commands.slash_command(
        description="edit the bot's configuration for this server",
    )
    @commands.has_permissions(manage_guild=True)
    async def config(self, inter: GuildCommandInteraction):
        guild = inter.guild
        assert guild is not None

        settings = await self.db.get_guild_settings(guild.id)
        embed = Embed(title=f"{WRENCH_EMOJI} configuration options")

        if settings.leveling == 0:
            emojistring = CROSS_EMOJI
        else:
            emojistring = CHECK_EMOJI
        embed.add_field(name=f"{STAR_EMOJI} leveling system", value=emojistring)

        if settings.welcoming != 0:
            channel = guild.get_channel(int(settings.welcoming))
            assert channel is not None
            embed.add_field(
                name=f"{WELCOME_EMOJI} welcome messages", value=channel.mention
            )
        else:
            embed.add_field(name=f"{WELCOME_EMOJI} welcome messages", value=CROSS_EMOJI)

        view = ConfigView(
            author_id=inter.author.id,
            db=self.db,
            bot=self.bot,
            guild=guild,
            config_inter=inter,
        )
        await inter.send(embed=embed, view=view, ephemeral=True)


def setup(bot: Megaton):
    bot.add_cog(Config(bot))
