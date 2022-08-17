from typing import Optional

from pydantic import BaseModel, HttpUrl


# Shared properties
class ImageURIBase(BaseModel):
    small: Optional[HttpUrl] = None
    normal: Optional[HttpUrl] = None
    large: Optional[HttpUrl] = None
    png: Optional[HttpUrl] = None
    art_crop: Optional[HttpUrl] = None
    border_crop: Optional[HttpUrl] = None
    card_id: Optional[int] = None


# Properties to receive on ImageURI creation
class ImageURICreate(ImageURIBase):
    pass


# Properties to receive on ImageURI update
class ImageURIUpdate(ImageURIBase):
    pass


# Properties shared by models stored in DB
class ImageURIInDBBase(ImageURIBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class ImageURI(ImageURIInDBBase):
    pass


# Properties properties stored in DB
class ImageURIInDB(ImageURIInDBBase):
    pass
