from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    ForeignKey,
    DateTime,
    Boolean,
    Integer,
    String,
    DECIMAL,
)
from sqlalchemy.sql import func

from app.db.base_class import Base

if TYPE_CHECKING:
    from .card_price import CardPrice  # noqa: F401


class CardPrice(Base):
    id = Column(Integer, primary_key=True, index=True)
    price = Column(DECIMAL, index=True)
    quantity = Column(Integer, index=True)
    condition = Column(String)
    is_foil = Column(Boolean)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    card_id = Column(Integer, ForeignKey("card.id"))
    store_id = Column(Integer, ForeignKey("store.id"))
