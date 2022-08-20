from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.models.store import Store
from app.schemas.store import StoreCreate
from app.tests.utils.utils import random_lower_string, random_url


def create_random_store(
    db: Session,
    *,
    name: Optional[str] = None,
    affiliate_code: Optional[str] = None,
    website: Optional[str] = None,
) -> Store:
    if name is None:
        name = random_lower_string()
    if affiliate_code is None:
        affiliate_code = random_lower_string()
    if website is None:
        website = random_url()

    store_in = StoreCreate(name=name, affiliate_code=affiliate_code, website=website,)
    return crud.store.create(db=db, obj_in=store_in)
