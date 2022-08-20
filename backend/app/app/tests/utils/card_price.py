from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.models.card_price import CardPrice
from app.schemas.card_price import CardPriceCreate
from app.tests.utils.utils import (
    random_lower_string,
    random_price,
    random_integer,
    random_boolean,
)
from app.tests.utils.card import create_card
from app.tests.utils.store import create_random_store


def create_random_card_price(
    db: Session,
    *,
    price: Optional[Decimal] = None,
    quantity: Optional[int] = None,
    condition: Optional[str] = None,
    is_foil: Optional[bool] = None,
    card_id: Optional[int] = None,
    store_id: Optional[int] = None,
) -> CardPrice:
    if price is None:
        price = random_price()
    if quantity is None:
        quantity = random_integer()
    if condition is None:
        condition = random_lower_string()
    if is_foil is None:
        is_foil = random_boolean()
    if card_id is None:
        card_id = create_card(db=db).id
    if store_id is None:
        store_id = create_random_store(db=db).id

    card_price_in = CardPriceCreate(
        price=price,
        quantity=quantity,
        condition=condition,
        is_foil=is_foil,
        card_id=card_id,
        store_id=store_id,
    )
    return crud.card_price.create(db=db, obj_in=card_price_in)
