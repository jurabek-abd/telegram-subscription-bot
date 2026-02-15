import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from loguru import logger

from config import config
from database.repository import UserRepository

logger.remove()
logger.add(sink=sys.stderr, level="INFO")
logger.add(sink="logs/bot.log", level="DEBUG", rotation="10 MB", compression="zip")

dp = Dispatcher()


@dp.startup()
async def on_startup(bot: Bot) -> None:
    """Log bot startup"""
    bot_info = await bot.get_me()
    logger.info(f"Bot started as @{bot_info.username}")


@dp.shutdown()
async def on_shutdown() -> None:
    """Log bot shutdown"""
    logger.info("Bot stopped")


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Handle /start command.
    """
    logger.info(f"User {message.from_user.id} started the bot")
    user = await UserRepository.get_by_telegram_id(message.from_user.id)

    if user is None:
        logger.info(f"User {message.from_user.id} is new")
        await UserRepository.create_user(
            message.from_user.id, message.from_user.username
        )
    else:
        logger.info(f"User {message.from_user.id} is already registered")
        await message.answer("Welcome back!")
        return

    await message.answer("Hey There!")


async def main() -> None:
    """
    Main function."""
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
    finally:
        await bot.session.close()
        await logger.complete()


if __name__ == "__main__":
    """Main entry point."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
