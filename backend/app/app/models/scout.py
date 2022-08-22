from typing import TYPE_CHECKING

from sqlalchemy import (
    Column,
    Enum,
    DECIMAL,
    ForeignKey,
    String,
    DateTime,
    Integer,
    Boolean,
)
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.schemas.scout import ScoutType

if TYPE_CHECKING:
    from .scout import Scout  # noqa: F401


class Scout(Base):
    id = Column(Integer, primary_key=True, index=True)
    scout_type = Column(String)
    price = Column(DECIMAL, index=True)
    quantity = Column(Integer)
    condition = Column(String)
    foil = Column(Boolean)
    nonfoil = Column(Boolean)
    first_created = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    card_id = Column(Integer, ForeignKey("card.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
