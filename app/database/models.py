import asyncio
from os import environ
from uuid import uuid4

from asyncpg import Connection as asyncpg_connection
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import (
    Boolean,
    TIMESTAMP,
    BigInteger,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

logger.info("Loading variables from .env file")
load_dotenv()

connection_string = (
    environ.get("DATABASE_URL", "")
    .replace("sqlite://", "sqlite+aiosqlite://")
    .replace("postgres://", "postgresql+asyncpg://")
    .replace("postgresql://", "postgresql+asyncpg://")
)

connection_args = {}
if "postgresql+asyncpg://" in connection_string:
    # https://github.com/sqlalchemy/sqlalchemy/issues/6467#issuecomment-864943824
    class Connection(asyncpg_connection):
        def _get_unique_id(self, prefix: str) -> str:
            return f"__asyncpg_{prefix}_{uuid4()}__"

    connection_args = {
        "connection_class": Connection,
    }

Base = declarative_base()

engine = create_async_engine(
    connection_string,
    connect_args=connection_args,
)
Session = sessionmaker(bind=engine, class_=AsyncSession)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, index=True)
    user_type = Column(String, nullable=False)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    referrer = Column(String)
    join_date = Column(TIMESTAMP, server_default=func.current_timestamp(), index=True)
    last_active = Column(TIMESTAMP, server_default=func.current_timestamp())

    setting = relationship("Setting", uselist=False, back_populates="user")


class Setting(Base):
    __tablename__ = "settings"

    user_id = Column(
        BigInteger, ForeignKey("users.user_id"), primary_key=True, index=True
    )
    language = Column(String, default="english")
    playlist_mode = Column(String, default="m3u")
    total_refer = Column(Integer, nullable=False, default=0)
    default_account  = Column(Integer)

    user = relationship("User", back_populates="setting", foreign_keys=[user_id])

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(BigInteger, nullable=False, primary_key=True)
    user_id = Column(
        BigInteger, ForeignKey("users.user_id"), index=True, primary_key=True
    )
    username = Column(String, nullable=False)
    token = Column(String, nullable=False)
    email = Column(String)
    password = Column(String)
    cookie = Column(String)
    is_premium = Column(Boolean)
    invites_remaining = Column(Integer)
    timestamp = Column(TIMESTAMP, server_default=func.current_timestamp())
    
class Admin(Base):
    __tablename__ = "admins"

    user_id = Column(BigInteger, primary_key=True, index=True)
    date = Column(TIMESTAMP, server_default=func.current_timestamp())


async def init_models():
    logger.info("Creating metadata for database")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
if __name__ == "__main__":
    asyncio.run(init_models())