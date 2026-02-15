from datetime import datetime
from typing import Optional

from sqlalchemy import and_, delete, exists, func, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import async_session_maker
from database.models import SubscriptionTier, User


class UserRepository:
    """Repository for User model."""

    # ============ CREATE ============

    @staticmethod
    async def create_user(telegram_id: int, username: Optional[str] = None) -> User:
        """Create a new user."""
        async with async_session_maker() as session:
            user = User(telegram_id=telegram_id, username=username)
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

    # ============ READ ============

    @staticmethod
    async def get_by_telegram_id(telegram_id: int) -> Optional[User]:
        """Get a user by their Telegram ID."""
        async with async_session_maker() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
