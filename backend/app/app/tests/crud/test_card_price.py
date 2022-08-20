from sqlalchemy.orm import Session

from app import crud
from app.schemas.card_price import CardPriceCreate, CardPriceUpdate
from app.tests.utils.card_price import create_random_card_price
from app.tests.utils.card import create_card
from app.tests.utils.store import create_random_store
from app.tests.utils.utils import (
    random_lower_string,
    random_boolean,
    random_integer,
    random_price,
)


def test_create_card_price(db: Session) -> None:
    # Create card and store
    card = create_card(db=db)
    store = create_random_store(db=db)

    # Define values
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    is_foil = random_boolean()
    card_id = card.id
    store_id = store.id

    # Build create schema
    card_price_in = CardPriceCreate(
        price=price,
        quantity=quantity,
        condition=condition,
        is_foil=is_foil,
        card_id=card_id,
        store_id=store_id,
    )
    # Create card_price
    card_price = crud.card_price.create(db=db, obj_in=card_price_in)

    # Check values
    assert card_price.price == price
    assert card_price.quantity == quantity
    assert card_price.condition == condition
    assert card_price.is_foil == is_foil
    assert card_price.card_id == card_id
    assert card_price.store_id == store_id
    assert card_price.first_seen

    # Clean-up
    crud.card_price.remove(db=db, id=card_price.id)
    crud.store.remove(db=db, id=store.id)
    crud.card.remove(db=db, id=card.id)


def test_get_card_price(db: Session) -> None:
    # Create card_price
    card_price = create_random_card_price(db=db)

    # Query created card_price
    stored_card_price = crud.card_price.get(db=db, id=card_price.id)

    # Check values
    assert stored_card_price
    assert card_price.id == stored_card_price.id
    assert card_price.price == stored_card_price.price
    assert card_price.quantity == stored_card_price.quantity
    assert card_price.condition == stored_card_price.condition
    assert card_price.is_foil == stored_card_price.is_foil
    assert card_price.first_seen == stored_card_price.first_seen
    assert card_price.last_updated == stored_card_price.last_updated
    assert card_price.card_id == stored_card_price.card_id
    assert card_price.store_id == stored_card_price.store_id

    # Clean-up
    crud.card_price.remove(db=db, id=card_price.id)
    crud.store.remove(db=db, id=card_price.store_id)
    crud.card.remove(db=db, id=card_price.card_id)


def test_update_card_price(db: Session) -> None:
    # Create card and store
    card = create_card(db=db)
    store = create_random_store(db=db)

    # Define values
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    is_foil = random_boolean()
    card_id = card.id
    store_id = store.id

    # Build create schema
    card_price_in = CardPriceCreate(
        price=price,
        quantity=quantity,
        condition=condition,
        is_foil=is_foil,
        card_id=card_id,
        store_id=store_id,
    )
    # Create card_price
    card_price = crud.card_price.create(db=db, obj_in=card_price_in)

    # Define new field and avoid the same value
    new_quantity = random_integer()
    while new_quantity == quantity:
        new_quantity = random_integer()

    # Build update schema
    card_price_update = CardPriceUpdate(quantity=new_quantity)

    # Update card_price
    card_price2 = crud.card_price.update(
        db=db, db_obj=card_price, obj_in=card_price_update
    )

    # Check values
    assert card_price.id == card_price2.id
    assert card_price.price == card_price2.price
    assert card_price2.quantity != quantity
    assert card_price2.quantity == new_quantity
    assert card_price2.last_updated

    # Clean-up
    crud.card_price.remove(db=db, id=card_price.id)
    crud.store.remove(db=db, id=store.id)
    crud.card.remove(db=db, id=card.id)


def test_delete_card_price(db: Session) -> None:
    # Create card and store
    card = create_card(db=db)
    store = create_random_store(db=db)

    # Define values
    price = random_price()
    quantity = random_integer()
    condition = random_lower_string()
    is_foil = random_boolean()
    card_id = card.id
    store_id = store.id

    # Build create schema
    card_price_in = CardPriceCreate(
        price=price,
        quantity=quantity,
        condition=condition,
        is_foil=is_foil,
        card_id=card_id,
        store_id=store_id,
    )
    # Create card_price
    card_price = crud.card_price.create(db=db, obj_in=card_price_in)

    # Delete card_price
    card_price2 = crud.card_price.remove(db=db, id=card_price.id)

    # Try querying deleted card_price
    card_price3 = crud.card_price.get(db=db, id=card_price.id)

    assert card_price3 is None

    # Check values
    assert card_price2.id == card_price.id
    assert card_price.price == price
    assert card_price.quantity == quantity
    assert card_price.condition == condition
    assert card_price.is_foil == is_foil
    assert card_price.card_id == card_id
    assert card_price.store_id == store_id

    ## Cleanup
    crud.store.remove(db=db, id=store.id)
    crud.card.remove(db=db, id=card.id)
