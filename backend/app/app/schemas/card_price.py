from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


# Shared properties
class CardPriceBase(BaseModel):
    price: Optional[Decimal]
    quantity: Optional[int]
    condition: Optional[str]
    is_foil: Optional[bool]
    card_id: Optional[int]
    store_id: Optional[int]


# Properties to receive on card_price creation
class CardPriceCreate(CardPriceBase):
    price: Decimal
    quantity: int
    card_id: int
    store_id: int


# Properties to receive on card_price update
class CardPriceUpdate(CardPriceBase):
    pass


# Properties shared by models stored in DB
class CardPriceInDBBase(CardPriceBase):
    id: int
    first_seen: datetime
    last_updated: Optional[datetime]

    class Config:
        orm_mode = True


# Properties to return to client
class CardPrice(CardPriceInDBBase):
    pass


# Additional properties stored in DB
class CardPriceInDB(CardPriceInDBBase):
    pass
