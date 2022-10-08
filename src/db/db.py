from __future__ import annotations
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import BigInteger, Integer, Column
from os import environ
from typing import Optional
from cachetools import TTLCache

Base = declarative_base()
engine = create_async_engine(url=environ["DB_URL"])
session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Serializable:
    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def deserialize(self, data: dict):
        return self(**data)

class EconomyData(Base, Serializable):  # type: ignore
    __tablename__ = "economy"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    wallet = Column(Integer, nullable=False, default=0)
    bank = Column(Integer, nullable=False, default=0)
    cache: TTLCache[int, bytes] = TTLCache(maxsize=100, ttl=60)

    @classmethod
    async def update_wallet(cls, item_id: int, wallet_amount: int) -> None:
        r = await cls.get(item_id)
        async with session() as s:
            r.wallet += wallet_amount
            await s.commit()
            cls.cache[item_id] = r.serialize()

    @classmethod
    async def get(cls, item_id: int) -> EconomyData:
        if item_id in cls.cache:
            return cls.from_data(cls.cache[item_id])
        query = select(cls).where(cls.id == item_id)
        async with session() as s:
            results = await s.execute(query)
            if not (result := results.first()):
                d = EconomyData(id=item_id, wallet=0, bank=0, bank_capacity=20000)
                s.add(d)
                await s.commit()
                cls.cache[item_id] = d.serialize()
                return d

            cls.cache[item_id] = result[0].serialize()

        return result[0]

    @classmethod
    async def update_bank(cls, item_id: int, bank_amount: int) -> None:
        async with session() as s:
            eco = await cls.get(item_id)
            eco.bank = bank_amount
            await s.commit()
            cls.cache[item_id] = eco.serialize()

    @classmethod
    async def withdraw(cls, item_id: int, amount: int) -> None:
        async with session() as s:
            eco = await cls.get(item_id)
            eco.wallet += amount
            eco.bank -= amount
            await s.commit()
            cls.cache[item_id] = eco.serialize()

    @classmethod
    async def deposit(cls, item_id: int, amount: int) -> None:
        async with session() as s:
            eco = await cls.get(item_id)
            eco.wallet -= amount
            eco.bank += amount
            await s.commit()
            cls.cache[item_id] = eco.serialize()

    def __repr__(self):
        return f"<EconomyData(id={self.id})>"


class GuildSettings(Base, Serializable):  # type: ignore
    __tablename__ = "guild_settings"
    guild_id = Column(BigInteger, primary_key=True)
    leveling = Column(BigInteger, nullable=True)
    logging = Column(BigInteger, nullable=True)
    welcoming = Column(BigInteger, nullable=True)
    autorole = Column(BigInteger, nullable=True)
    cache: TTLCache[int, bytes] = TTLCache(maxsize=100, ttl=60)

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