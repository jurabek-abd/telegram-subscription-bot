"""
Development script to create database tables.
Run this once to set up your database schema.

WARNING: This drops all existing tables first!
"""

import asyncio
import sys

from loguru import logger

from database.engine import Base, engine
from database.models import User


async def create_tables():
    """
    Create database tables.
    """

    logger.info("Creating database tables...")

    try:
        async with engine.begin() as conn:
            logger.info("Dropping existing tables...")
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("Creating tables...")
            await conn.run_sync(Base.metadata.create_all)

        logger.success("Tables created successfully!")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(create_tables())
