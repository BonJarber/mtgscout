from distutils.util import strtobool
from sqlalchemy.orm import Session

from app import crud
from app.schemas.card import CardCreate, CardUpdate
from app.tests.utils.card import TestData, create_card
from app.tests.utils.utils import random_lower_string


def test_create_card(db: Session) -> None:
    card_in = CardCreate(
        scryfall_id=TestData.scryfall_id.value,
        oracle_id=TestData.oracle_id.value,
        mtgo_id=TestData.mtgo_id.value,
        mtgo_foil_id=TestData.mtgo_foil_id.value,
        tcgplayer_id=TestData.tcgplayer_id.value,
        cardmarket_id=TestData.cardmarket_id.value,
        name=TestData.name.value,
        lang=TestData.lang.value,
        foil=TestData.foil.value,
        nonfoil=TestData.nonfoil.value,
        set_id=TestData.set_id.value,
        set_shortname=TestData.set_shortname.value,
        set_name=TestData.set_name.value,
        rarity=TestData.rarity.value,
        reserved=TestData.reserved.value,
    )
    card = crud.card.create(db=db, obj_in=card_in)
    assert str(card.scryfall_id) == str(TestData.scryfall_id.value)
    assert str(card.oracle_id) == str(TestData.oracle_id.value)
    assert card.mtgo_id == int(TestData.mtgo_id.value)
    assert card.mtgo_foil_id == int(TestData.mtgo_foil_id.value)
    assert card.tcgplayer_id == int(TestData.tcgplayer_id.value)
    assert card.cardmarket_id == int(TestData.cardmarket_id.value)
    assert card.name == TestData.name.value
    assert card.lang == TestData.lang.value
    assert card.foil == strtobool(TestData.foil.value)
    assert card.nonfoil == strtobool(TestData.nonfoil.value)
    assert str(card.set_id) == str(TestData.set_id.value)
    assert card.set_shortname == TestData.set_shortname.value
    assert card.set_name == TestData.set_name.value
    assert card.rarity == TestData.rarity.value
    assert card.reserved == strtobool(TestData.reserved.value)


def test_get_card(db: Session) -> None:
    card = create_card(db=db)
    stored_card = crud.card.get(db=db, id=card.id)
    assert stored_card
    assert str(card.scryfall_id) == str(stored_card.scryfall_id)
    assert str(card.oracle_id) == str(stored_card.oracle_id)
    assert card.mtgo_id == stored_card.mtgo_id
    assert card.mtgo_foil_id == stored_card.mtgo_foil_id
    assert card.tcgplayer_id == stored_card.tcgplayer_id
    assert card.cardmarket_id == stored_card.cardmarket_id
    assert card.name == stored_card.name
    assert card.lang == stored_card.lang
    assert card.foil == stored_card.foil
    assert card.nonfoil == stored_card.nonfoil
    assert str(card.set_id) == str(stored_card.set_id)
    assert card.set_shortname == stored_card.set_shortname
    assert card.set_name == stored_card.set_name
    assert card.rarity == stored_card.rarity
    assert card.reserved == stored_card.reserved


def test_update_card(db: Session) -> None:
    card = create_card(db=db)
    name2 = random_lower_string()
    card_update = CardUpdate(name=name2)
    card2 = crud.card.update(db=db, db_obj=card, obj_in=card_update)
    assert card.id == card2.id
    assert card.mtgo_id == card2.mtgo_id
    assert card2.name == name2
    assert card.rarity == card2.rarity


def test_delete_card(db: Session) -> None:
    card = create_card(db=db)
    card2 = crud.card.remove(db=db, id=card.id)
    card3 = crud.card.get(db=db, id=card.id)
    assert card3 is None
    assert card2.id == card.id
    assert card2.name == TestData.name
    assert card2.tcgplayer_id == int(TestData.tcgplayer_id.value)
