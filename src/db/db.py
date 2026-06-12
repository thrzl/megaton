from __future__ import annotations
from typing import Optional
from aiosqlite import connect as sqlite
from msgspec import Struct

class Database:
    __slots__ = ("client",)
    def __init__(self, db_url: str):
        self.client = sqlite(db_url)

    async def get_economy_data(self, item_id: int) -> EconomyData:
        async with self.client as db:
            results = await db.execute("SELECT * FROM economy_data WHERE id = ?", (item_id,))
            row = await results.fetchone()
            if row is None:
                new_row = EconomyData(_db=self, id=item_id, wallet=0, bank=0)
                await db.execute("INSERT INTO economy_data (id, wallet, bank) VALUES (?, ?, ?)", (new_row.id, new_row.wallet, new_row.bank))
                await db.commit()
                return new_row

            return EconomyData(_db=self, id=row["id"], wallet=row["wallet"], bank=row["bank"])
            
class DatabaseModel(Struct):
    _db: Database

class EconomyData(DatabaseModel):
    id: int
    wallet: int
    bank: int

    async def update_wallet(self, wallet_amount: int) -> None:
        async with self._db.client as db:
            self.wallet += wallet_amount
            await db.execute("UPDATE economy_data SET wallet = wallet + ? WHERE id = ?", (wallet_amount, self.id))
            await db.commit()

    async def update_bank(self, bank_amount: int) -> None:
        async with self._db.client as db:
            self.bank += bank_amount
            await db.execute("UPDATE economy_data SET bank = bank + ? WHERE id = ?", (bank_amount, self.id))
            await db.commit()

    async def withdraw(self, amount: int) -> None:
        async with self._db.client as db:
            self.wallet += amount
            self.bank -= amount
            await db.execute("UPDATE economy_data SET wallet = wallet + ?, bank = bank - ? WHERE id = ?", (amount, amount, self.id))
            await db.commit()

    async def deposit(self, amount: int) -> None:
        async with self._db.client as db:
            self.wallet -= amount
            self.bank += amount
            await db.execute("UPDATE economy_data SET wallet = wallet - ?, bank = bank + ? WHERE id = ?", (amount, amount, self.id))
            await db.commit()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class DatabaseModel(Struct):
    def __init__(self, db, **kwargs):
        self.db = db
        for k, v in kwargs.items():
            setattr(self, k, v)

class GuildSettings(Base):  # type: ignore
    __tablename__ = "guild_settings"
    guild_id = Column(BigInteger, primary_key=True)
    leveling = Column(BigInteger, nullable=True)
    logging = Column(BigInteger, nullable=True)
    welcoming = Column(BigInteger, nullable=True)
    autorole = Column(BigInteger, nullable=True)

    @classmethod
    async def update_leveling_channel(cls, guild_id: int, channel_id: int):
        g_settings = await cls.get(guild_id)
        async with session() as s:
            if not g_settings:
                s.add(GuildSettings(guild_id=guild_id, leveling=channel_id))
                await s.commit()
            else:
                g_settings.leveling = channel_id
                await s.commit()

    @classmethod
    async def update_logging_channel(cls, guild_id: int, channel_id: int):
        g_settings = await cls.get(guild_id)
        async with session() as s:
            if not g_settings:
                s.add(GuildSettings(guild_id=guild_id, logging=channel_id))
                await s.commit()
            else:
                g_settings.logging = channel_id
                await s.commit()

    @classmethod
    async def update_welcoming_channel(cls, guild_id: int, channel_id: int):
        g_settings = await cls.get(guild_id)
        async with session() as s:
            if not g_settings:
                s.add(GuildSettings(guild_id=guild_id, welcoming=channel_id))
                await s.commit()
            else:
                g_settings.welcoming = channel_id
                await s.commit()

    @classmethod
    async def update_autorole(cls, guild_id: int, role_id: int) -> None:
        g_settings = await cls.get(guild_id)
        async with session() as s:
            if not g_settings:
                s.add(GuildSettings(guild_id=guild_id, autorole=role_id))
                await s.commit()
            else:
                g_settings.autorole = role_id
                await s.commit()

    @classmethod
    async def get(cls, guild_id: int) -> Optional[GuildSettings]:
        if data := cls.cache.get(guild_id):
            return cls.from_data(data)
        query = select(cls).where(cls.guild_id == guild_id)
        async with session() as s:
            results = await s.execute(query)
            if not (result := results.first()):
                return None
            cls.cache[guild_id] = result[0].serialize()
        return result[0]

    def __repr__(self):
        return f"<GuildSettings(guild_id={self.guild_id})>"
