import enum
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from database.engine import Base


class SubscriptionTier(enum.Enum):
    """Different subscription tiers available."""

    FREE = "FREE"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"


class User(Base):
    """User model representing a Telegram user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subscription_tier: Mapped[SubscriptionTier] = mapped_column(
        Enum(SubscriptionTier), default=SubscriptionTier.FREE, nullable=False
    )
    subscription_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
    )

    def __repr__(self):
        """How the user looks when you print it"""
        return f"<User(telegram_id={self.telegram_id}, tier={self.subscription_tier.value})>"
