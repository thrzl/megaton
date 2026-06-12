from __future__ import annotations
from aiosqlite import connect as sqlite, Connection
from msgspec import Struct


class Database:
    __slots__ = ("client",)

    def __init__(self, connection: Connection):
        self.client = connection

    @classmethod
    async def create(cls, db_url: str) -> Database:
        self = cls(await sqlite(db_url))
        await self.client.execute(
            "CREATE TABLE IF NOT EXISTS economy_data (id INTEGER PRIMARY KEY, wallet INTEGER, bank INTEGER)"
        )
        await self.client.execute(
            "CREATE TABLE IF NOT EXISTS guild_settings (guild_id INTEGER PRIMARY KEY, leveling INTEGER, logging INTEGER, welcoming INTEGER)"
        )
        return self

    async def get_economy_data(self, item_id: int) -> EconomyData:
        results = await self.client.execute(
            "SELECT * FROM economy_data WHERE id = ?", (item_id,)
        )
        row = await results.fetchone()
        if row is None:
            new_row = EconomyData(_db=self, id=item_id, wallet=0, bank=0)
            await self.client.execute(
                "INSERT INTO economy_data (id, wallet, bank) VALUES (?, ?, ?)",
                (new_row.id, new_row.wallet, new_row.bank),
            )
            await self.client.commit()
            return new_row

        return EconomyData(_db=self, id=row[0], wallet=row[1], bank=row[2])

    async def get_guild_settings(self, guild_id: int) -> GuildSettings:
        results = await self.client.execute(
            "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
        )
        row = await results.fetchone()
        if row is None:
            new_row = GuildSettings(
                _db=self, guild_id=guild_id, leveling=0, logging=0, welcoming=0
            )
            await self.client.execute(
                "INSERT INTO guild_settings (guild_id, leveling, logging, welcoming) VALUES (?, ?, ?, ?)",
                (
                    new_row.guild_id,
                    new_row.leveling,
                    new_row.logging,
                    new_row.welcoming,
                ),
            )
            await self.client.commit()
            return new_row

        return GuildSettings(
            _db=self,
            guild_id=row[0],
            leveling=row[1],
            logging=row[2],
            welcoming=row[3],
        )


class DatabaseModel(Struct):
    _db: Database


class EconomyData(DatabaseModel):
    id: int
    wallet: int
    bank: int

    async def update_wallet(self, wallet_amount: int) -> None:
        self.wallet += wallet_amount
        await self._db.client.execute(
            "UPDATE economy_data SET wallet = wallet + ? WHERE id = ?",
            (wallet_amount, self.id),
        )
        await self._db.client.commit()

    async def update_bank(self, bank_amount: int) -> None:
        self.bank += bank_amount
        await self._db.client.execute(
            "UPDATE economy_data SET bank = bank + ? WHERE id = ?",
            (bank_amount, self.id),
        )
        await self._db.client.commit()

    async def withdraw(self, amount: int) -> None:
        self.wallet += amount
        self.bank -= amount
        await self._db.client.execute(
            "UPDATE economy_data SET wallet = wallet + ?, bank = bank - ? WHERE id = ?",
            (amount, amount, self.id),
        )
        await self._db.client.commit()

    async def deposit(self, amount: int) -> None:
        self.wallet -= amount
        self.bank += amount
        await self._db.client.execute(
            "UPDATE economy_data SET wallet = wallet - ?, bank = bank + ? WHERE id = ?",
            (amount, amount, self.id),
        )
        await self._db.client.commit()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(DatabaseModel):
    guild_id: int
    leveling: int
    logging: int
    welcoming: int

    async def update_leveling_channel(self, channel_id: int):
        self.leveling = channel_id
        await self._db.client.execute(
            "UPDATE guild_settings SET leveling = ? WHERE guild_id = ?",
            (channel_id, self.guild_id),
        )
        await self._db.client.commit()

    async def update_logging_channel(self, channel_id: int):
        self.logging = channel_id
        await self._db.client.execute(
            "UPDATE guild_settings SET logging = ? WHERE guild_id = ?",
            (channel_id, self.guild_id),
        )
        await self._db.client.commit()

    async def update_welcoming_channel(self, channel_id: int):
        self.welcoming = channel_id
        await self._db.client.execute(
            "UPDATE guild_settings SET welcoming = ? WHERE guild_id = ?",
            (channel_id, self.guild_id),
        )
        await self._db.client.commit()

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
