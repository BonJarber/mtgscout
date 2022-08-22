from sqlalchemy.orm import Session

from app import crud
from app.schemas.scout import ScoutCreate, ScoutUpdate, ScoutType
from app.tests.utils.card import create_card
from app.tests.utils.scout import create_random_scout
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import (
    random_lower_string,
    random_price,
    random_integer,
    random_boolean,
)


def test_create_scout(db: Session) -> None:
    # Define values
    scout_type = ScoutType.price
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    foil = random_boolean()
    nonfoil = random_boolean()
    card_id = create_card(db=db).id
    user_id = create_random_user(db=db).id

    # Build create schema
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
    # Create scout
    scout = crud.scout.create(db=db, obj_in=scout_in)

    # Check values
    assert scout.scout_type == scout_type
    assert scout.price == price
    assert scout.quantity == quantity
    assert scout.condition == condition
    assert scout.foil == foil
    assert scout.nonfoil == nonfoil
    assert scout.first_created
    assert scout.card_id == card_id
    assert scout.user_id == user_id

    # Clean-up
    crud.scout.remove(db=db, id=scout.id)
    crud.user.remove(db=db, id=scout.user_id)
    crud.card.remove(db=db, id=scout.card_id)


def test_get_scout(db: Session) -> None:
    # Create scout
    scout = create_random_scout(db=db)

    # Query created scout
    stored_scout = crud.scout.get(db=db, id=scout.id)

    # Check values
    assert stored_scout
    assert scout.id == stored_scout.id
    assert scout.scout_type == stored_scout.scout_type
    assert scout.price == stored_scout.price
    assert scout.quantity == stored_scout.quantity
    assert scout.condition == stored_scout.condition
    assert scout.foil == stored_scout.foil
    assert scout.nonfoil == stored_scout.nonfoil
    assert scout.first_created == stored_scout.first_created
    assert scout.last_updated == stored_scout.last_updated
    assert scout.card_id == stored_scout.card_id
    assert scout.user_id == stored_scout.user_id

    # Clean-up
    crud.scout.remove(db=db, id=scout.id)
    crud.user.remove(db=db, id=scout.user_id)
    crud.card.remove(db=db, id=scout.card_id)


def test_update_scout(db: Session) -> None:
    # Define values
    scout_type = ScoutType.price.value
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    foil = random_boolean()
    nonfoil = random_boolean()
    card_id = create_card(db=db).id
    user_id = create_random_user(db=db).id

    # Build create schema
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
    # Create scout
    scout = crud.scout.create(db=db, obj_in=scout_in)

    # Define new field
    new_price = random_price()

    # Build update schema
    scout_update = ScoutUpdate(price=new_price)

    # Update scout
    scout2 = crud.scout.update(db=db, db_obj=scout, obj_in=scout_update)

    # Check values
    assert scout.id == scout2.id
    assert scout2.last_updated
    assert scout.quantity == scout2.quantity
    assert scout2.price != price
    assert scout2.price == new_price

    # Clean-up
    crud.scout.remove(db=db, id=scout.id)
    crud.user.remove(db=db, id=user_id)
    crud.card.remove(db=db, id=card_id)


def test_delete_scout(db: Session) -> None:
    # Define values
    scout_type = ScoutType.price.value
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    foil = random_boolean()
    nonfoil = random_boolean()
    card_id = create_card(db=db).id
    user_id = create_random_user(db=db).id

    # Build create schema
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
    # Create scout
    scout = crud.scout.create(db=db, obj_in=scout_in)

    # Delete scout
    scout2 = crud.scout.remove(db=db, id=scout.id)

    # Try querying deleted scout
    scout3 = crud.scout.get(db=db, id=scout.id)

    assert scout3 is None

    # Check values
    assert scout2.id == scout.id
    assert scout.scout_type == scout_type
    assert scout.price == price
    assert scout.quantity == quantity
    assert scout.condition == condition
    assert scout.foil == foil
    assert scout.nonfoil == nonfoil
    assert scout.card_id == card_id
    assert scout.user_id == user_id

    crud.card.remove(db=db, id=scout.card_id)
    crud.user.remove(db=db, id=scout.user_id)
