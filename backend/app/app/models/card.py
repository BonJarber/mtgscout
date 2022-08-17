from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.schemas.card import Rarity


class Card(Base):
    id = Column(Integer, primary_key=True, index=True)
    scryfall_id = Column(UUID(as_uuid=True))
    oracle_id = Column(UUID(as_uuid=True), index=True)
    mtgo_id = Column(Integer)
    mtgo_foil_id = Column(Integer)
    tcgplayer_id = Column(Integer)
    cardmarket_id = Column(Integer)
    name = Column(String, index=True)
    lang = Column(String, index=True)
    foil = Column(Boolean)
    nonfoil = Column(Boolean)
    set_id = Column(UUID(as_uuid=True))
    set_shortname = Column(String)
    set_name = Column(String)
    rarity = Column(Enum(Rarity))
    reserved = Column(Boolean)

    image_uris = relationship(
        "ImageURI", cascade="all, delete-orphan", backref="card", lazy="dynamic"
    )

