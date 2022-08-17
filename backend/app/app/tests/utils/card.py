from uuid import UUID
from enum import Enum
from sqlalchemy.orm import Session

from app import crud
from app.schemas.card import CardCreate, Rarity


class TestData(str, Enum):
    scryfall_id = UUID("0000579f-7b35-4ed3-b44c-db2a538066fe")
    oracle_id = UUID("44623693-51d6-49ad-8cd7-140505caf02f")
    mtgo_id = 25527
    mtgo_foil_id = 25528
    tcgplayer_id = 14240
    cardmarket_id = 13850
    name = "Fury Sliver"
    lang = "en"
    foil = True
    nonfoil = True
    set_id = UUID("c1d109bc-ffd8-428f-8d7d-3f8d7e648046")
    set_shortname = "tsp"
    set_name = "Time Spiral"
    rarity = Rarity.uncommon.value
    reserved = False


def create_card(db: Session):
    card_in = CardCreate(
        scryfall_id=TestData.scryfall_id,
        oracle_id=TestData.oracle_id,
        mtgo_id=TestData.mtgo_id,
        mtgo_foil_id=TestData.mtgo_foil_id,
        tcgplayer_id=TestData.tcgplayer_id,
        cardmarket_id=TestData.cardmarket_id,
        name=TestData.name,
        lang=TestData.lang,
        foil=TestData.foil,
        nonfoil=TestData.nonfoil,
        set_id=TestData.set_id,
        set_shortname=TestData.set_shortname,
        set_name=TestData.set_name,
        rarity=TestData.rarity,
        reserved=TestData.reserved,
    )
    return crud.card.create(db=db, obj_in=card_in)
