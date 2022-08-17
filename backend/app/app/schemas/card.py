from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, UUID4


class Rarity(str, Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    mythic = "mythic"


# Shared properties
class CardBase(BaseModel):
    scryfall_id: Optional[UUID4] = None
    oracle_id: Optional[UUID4] = None
    mtgo_id: Optional[int] = None
    mtgo_foil_id: Optional[int] = None
    tcgplayer_id: Optional[int] = None
    cardmarket_id: Optional[int] = None
    name: Optional[str] = None
    lang: Optional[str] = None
    foil: Optional[bool] = None
    nonfoil: Optional[bool] = None
    set_id: Optional[UUID4] = None
    set_shortname: Optional[str] = None
    set_name: Optional[str] = None
    rarity: Optional[Rarity] = None
    reserved: Optional[bool] = None


# Properties to receive on Card creation
class CardCreate(CardBase):
    pass


# Properties to receive on Card update
class CardUpdate(CardBase):
    pass


# Properties shared by models stored in DB
class CardInDBBase(CardBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Card(CardInDBBase):
    image_uri_ids: Optional[List[int]]


# Properties properties stored in DB
class CardInDB(CardInDBBase):
    pass
