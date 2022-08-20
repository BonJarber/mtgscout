from typing import Optional

from pydantic import BaseModel, HttpUrl


# Shared properties
class StoreBase(BaseModel):
    name: Optional[str]
    affiliate_code: Optional[str]
    website: Optional[HttpUrl]


# Properties to receive on store creation
class StoreCreate(StoreBase):
    name: str
    website: Optional[HttpUrl]


# Properties to receive on store update
class StoreUpdate(StoreBase):
    pass


# Properties shared by models stored in DB
class StoreInDBBase(StoreBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Store(StoreInDBBase):
    pass


# Additional properties stored in DB
class StoreInDB(StoreInDBBase):
    pass
