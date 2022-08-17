from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.base_class import Base


class ImageURI(Base):
    id = Column(Integer, primary_key=True, index=True)
    small = Column(String)
    normal = Column(String)
    large = Column(String)
    png = Column(String)
    art_crop = Column(String)
    border_crop = Column(String)
    card_id = Column(Integer, ForeignKey("card.id"))
