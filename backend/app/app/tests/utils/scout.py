from decimal import Decimal
from typing import Optional

from sqlalchemy.orm import Session

from app import crud
from app.models.scout import Scout
from app.schemas.scout import ScoutCreate, ScoutType
from app.tests.utils.card import create_card
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import (
    random_lower_string,
    random_boolean,
    random_integer,
    random_price,
)


def create_random_scout(
    db: Session,
    *,
    scout_type: Optional[ScoutType] = None,
    price: Optional[Decimal] = None,
    quantity: Optional[int] = None,
    condition: Optional[str] = None,
    foil: Optional[bool] = None,
    nonfoil: Optional[bool] = None,
    card_id: Optional[int] = None,
    user_id: Optional[int] = None,
) -> Scout:
    if scout_type is None:
        scout_type = ScoutType.price
    if price is None:
        price = random_price()
    if quantity is None:
        quantity = random_integer()
    if condition is None:
        condition = random_lower_string()
    if foil is None:
        foil = random_boolean()
    if nonfoil is None:
        nonfoil = random_boolean()
    if card_id is None:
        card_id = create_card(db=db).id
    if user_id is None:
        user_id = create_random_user(db=db).id

    scout_in = ScoutCreate(
        scout_type=scout_type,
        price=price,
        quantity=quantity,
        condition=condition,
        foil=foil,
        nonfoil=nonfoil,
        card_id=card_id,
        user_id=user_id,
    )
    return crud.scout.create(db=db, obj_in=scout_in)
