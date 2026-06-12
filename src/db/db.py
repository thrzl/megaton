from __future__ import annotations
from aiosqlite import connect as sqlite
from msgspec import Struct


class Database:
    __slots__ = ("client",)

    def __init__(self, db_url: str):
        self.client = sqlite(db_url)

    async def get_economy_data(self, item_id: int) -> EconomyData:
        async with self.client as db:
            results = await db.execute(
                "SELECT * FROM economy_data WHERE id = ?", (item_id,)
            )
            row = await results.fetchone()
            if row is None:
                new_row = EconomyData(_db=self, id=item_id, wallet=0, bank=0)
                await db.execute(
                    "INSERT INTO economy_data (id, wallet, bank) VALUES (?, ?, ?)",
                    (new_row.id, new_row.wallet, new_row.bank),
                )
                await db.commit()
                return new_row

            return EconomyData(
                _db=self, id=row["id"], wallet=row["wallet"], bank=row["bank"]
            )

    async def get_guild_settings(self, guild_id: int) -> GuildSettings:
        async with self.client as db:
            results = await db.execute(
                "SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,)
            )
            row = await results.fetchone()
            if row is None:
                new_row = GuildSettings(
                    _db=self, guild_id=guild_id, leveling=0, logging=0, welcoming=0
                )
                await db.execute(
                    "INSERT INTO guild_settings (guild_id, leveling, logging, welcoming) VALUES (?, ?, ?, ?)",
                    (
                        new_row.guild_id,
                        new_row.leveling,
                        new_row.logging,
                        new_row.welcoming,
                    ),
                )
                await db.commit()
                return new_row

            return GuildSettings(
                _db=self,
                guild_id=row["guild_id"],
                leveling=row["leveling"],
                logging=row["logging"],
                welcoming=row["welcoming"],
            )


class DatabaseModel(Struct):
    _db: Database


class EconomyData(DatabaseModel):
    id: int
    wallet: int
    bank: int

    async def update_wallet(self, wallet_amount: int) -> None:
        async with self._db.client as db:
            self.wallet += wallet_amount
            await db.execute(
                "UPDATE economy_data SET wallet = wallet + ? WHERE id = ?",
                (wallet_amount, self.id),
            )
            await db.commit()

    async def update_bank(self, bank_amount: int) -> None:
        async with self._db.client as db:
            self.bank += bank_amount
            await db.execute(
                "UPDATE economy_data SET bank = bank + ? WHERE id = ?",
                (bank_amount, self.id),
            )
            await db.commit()

    async def withdraw(self, amount: int) -> None:
        async with self._db.client as db:
            self.wallet += amount
            self.bank -= amount
            await db.execute(
                "UPDATE economy_data SET wallet = wallet + ?, bank = bank - ? WHERE id = ?",
                (amount, amount, self.id),
            )
            await db.commit()

    async def deposit(self, amount: int) -> None:
        async with self._db.client as db:
            self.wallet -= amount
            self.bank += amount
            await db.execute(
                "UPDATE economy_data SET wallet = wallet - ?, bank = bank + ? WHERE id = ?",
                (amount, amount, self.id),
            )
            await db.commit()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(DatabaseModel):
    guild_id: int
    leveling: int
    logging: int
    welcoming: int

    async def update_leveling_channel(self, channel_id: int):
        async with self._db.client as db:
            self.leveling = channel_id
            await db.execute(
                "UPDATE guild_settings SET leveling = ? WHERE guild_id = ?",
                (channel_id, self.guild_id),
            )
            await db.commit()

    async def update_logging_channel(self, channel_id: int):
        async with self._db.client as db:
            self.logging = channel_id
            await db.execute(
                "UPDATE guild_settings SET logging = ? WHERE guild_id = ?",
                (channel_id, self.guild_id),
            )
            await db.commit()

    async def update_welcoming_channel(self, channel_id: int):
        async with self._db.client as db:
            self.welcoming = channel_id
            await db.execute(
                "UPDATE guild_settings SET welcoming = ? WHERE guild_id = ?",
                (channel_id, self.guild_id),
            )
            await db.commit()

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
