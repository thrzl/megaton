# AGENTS.md

Coding patterns and conventions for this codebase.

## General

- Variables should always have descriptive names — `interaction` is better than `inter`, `welcome_channel` is better than `wcm`
- Text literals should have a consistent tone — lowercase, casual, and friendly

## Disnake / Discord

### Embeds

Use the custom `Embed` class from `src.bot` — it lowercases everything by default (field names, values, titles, descriptions, footer text). Pass `preserve_case=True` when case must be preserved. This is largely to ensure that very old literals are lowercased automatically. New embeds should still use lowercase text.

```python
from src.bot import Embed

embed = Embed(title="your title", description="your description")
# title and description will be lowercased in the output in the event that they are not capitalized in the literal
```

### Emoji Constants

Use the constants from `src.utils.emojis` instead of raw emoji strings:

```python
from src.utils.emojis import CHECK_EMOJI, CROSS_EMOJI
```

### Slash Commands

Use the `@slash_command` decorator with explicit `name`, `description`, `usage`, and `aliases`:

```python
from disnake.ext.commands.slash_core import slash_command

@slash_command(
    name="command_name",
    description="What the command does.",
    usage="command_name <arg>",
    aliases=["alias1", "alias2"],
)
async def command_name(self, ctx: ApplicationCommandInteraction):
    ...
```

### Views and Interaction Checks

Views should validate that only the invoking user can interact with them:

```python
async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
    if interaction.author.id != self.author_id:
        await interaction.response.send_message(
            "You are not allowed to interact with this menu.", ephemeral=True
        )
        return False
    return True
```

### Bot Reference

Cogs store a reference to the bot instance:

```python
class MyCog(commands.Cog):
    def __init__(self, bot: Megaton):
        self.bot = bot
```

## Database

### Access

The `Database` instance lives at `Megaton.db`. Always assert it exists in a cog's `__init__` if the cog depends on the database:

```python
def __init__(self, bot: Megaton):
    self.bot = bot
    if bot.db is None:
        raise ValueError("database connection is not established.")
    self.db = bot.db
```

### Models

Data models inherit from `DatabaseModel` (a `msgspec.Struct`) and always include a `_db: Database` field:

```python
class EconomyData(DatabaseModel):
    id: int
    wallet: int
    bank: int

    _db: Database  # must be last, keyword-only
```

### Upsert Pattern

`get_*` methods should create a default row if none exists:

```python
async def get_guild_settings(self, guild_id: int) -> GuildSettings:
    row = await self.client.execute("SELECT * FROM ...", (guild_id,))
    if row is None:
        new_row = GuildSettings(_db=self, guild_id=guild_id, leveling=0, ...)
        await self.client.execute("INSERT INTO ...", ...)
        await self.client.commit()
        return new_row
    return GuildSettings(_db=self, ...)
```

### Async Only

All database operations are async. Never use blocking calls on the database.

## Cog Structure

Every cog file must end with a `setup` function:

```python
def setup(bot):
    bot.add_cog(MyCog(bot))
```

## Custom Exceptions

Bot-specific exceptions are defined in `src.bot`:

- `FalseVaccum` — invalid time format (e.g. not ending in `d`, `h`, `m`, `s`)
- `HeirarchyError` — hierarchy permission failures

## Type Hints

Use type hints throughout. Common patterns:

```python
guild: Optional[disnake.Guild] = inter.guild
assert guild is not None  # after checking with Optional[]
```
