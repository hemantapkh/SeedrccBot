import asyncio
from os import environ

import uvloop
import sentry_sdk
from loguru import logger
from pyrogram import Client, filters

from database import DataBase
from database.models import init_models

from plugins.functions.filters import Filter
from plugins.functions.keyboards import KeyBoard
from plugins.functions.misc import Misc

from languages.language import Language

# Initializing sentry for error tracking
if environ.get("SENTRY_DSN"):
    logger.info("Initializing sentry")
    sentry_sdk.init(
        dsn=environ.get("SENTRY_DSN"),
        environment=environ.get("ENVIRONMENT") or "local"
    )

# Installing UVloop for better performance
logger.info("Installing uvloop")
uvloop.install()

# Configure logger to write logs to file and console
log_file = environ.get("LOGFILE")
if log_file:
    logger.add(
        log_file,
        backtrace=True,
        rotation="10 MB",
    )

logger.info("Creating database instance")
Client.DB = DataBase()

logger.info("Creating bot instance")
bot = Client(
    name=environ.get("BOT_NAME") or "Torrent Seedr",
    api_id=environ.get("API_ID"),
    api_hash=environ.get("API_HASH"),
    bot_token=environ.get("BOT_TOKEN"),
    plugins=dict(root="plugins"),
    workdir=environ.get("WORKDIR"),
)

# Loading required instances in the Client
Client.misc = Misc(bot)
Client.keyboard = KeyBoard(bot)
Client.language = Language("languages/languages.json", "languages/translations.json")
filters.custom = Filter(bot)

async def main():
    async with bot:
        await init_models()

        logger.info("Getting bot information")
        me = await bot.get_me()
        Client.USERNAME = me.username

if __name__ == "__main__":
    bot.run(main())
    logger.info(f"Starting {environ.get('BOT_NAME')}")
    asyncio.run(bot.run())