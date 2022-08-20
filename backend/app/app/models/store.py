from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .store import Store  # noqa: F401


class Store(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    affiliate_code = Column(String, index=True)
    website = Column(String)

    prices = relationship(
        "CardPrice", cascade="all, delete-orphan", backref="store", lazy="dynamic"
    )
