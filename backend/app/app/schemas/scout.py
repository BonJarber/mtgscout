from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ScoutType(str, Enum):
    uncommon = "uncommon"
    price = "price"
    quantity = "quantity"
    buylist = "buylist"


# Shared properties
class ScoutBase(BaseModel):
    scout_type: Optional[ScoutType] = None
    price: Optional[Decimal]
    quantity: Optional[int]
    condition: Optional[str]
    foil: Optional[bool]
    nonfoil: Optional[bool]
    card_id: Optional[int]


# Properties to receive on scout creation
class ScoutCreate(ScoutBase):
    scout_type: ScoutType
    card_id: int
    user_id: int


# Properties to receive on scout creation
class ScoutApiCreate(ScoutBase):
    scout_type: str
    card_id: int


# Properties to receive on scout update
class ScoutUpdate(ScoutBase):
    pass


# Properties shared by models stored in DB
class ScoutInDBBase(ScoutBase):
    id: int
    first_created: datetime
    last_updated: Optional[datetime]
    user_id: Optional[int]

    class Config:
        orm_mode = True


# Properties to return to client
class Scout(ScoutInDBBase):
    first_created: datetime
    last_updated: Optional[datetime]


# Additional properties stored in DB
class ScoutInDB(ScoutInDBBase):
    pass
