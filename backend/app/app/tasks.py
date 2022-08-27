import json
import logging
import requests

from app.db.session import SessionLocal
from app.schemas.card import CardCreate, Card
from app import crud

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    try:
        # Try to create session to check if DB is awake
        db = SessionLocal()
        db.execute("SELECT 1")
        return db
    except Exception as e:
        logger.error(e)
        raise e


def check_scouts() -> None:
    db = init_db()
    skip = 0
    count = 0

    logger.info("Starting scout check")
    scouts = crud.scout.get_multi(db=db, skip=skip)
    while scouts:
        for scout in scouts:
            # Call celery task to check price
            count += 1

        skip += 100
        scouts = crud.scout.get_multi(db=db, skip=skip)

    logger.info(f"Finished, checked {count} scouts")
    return


def lookup_set_code(set_name: str) -> str:
    with open("app/assets/set_data.json") as f:
        sets = json.load(f)
    for s in sets:
        if s["name"] == set_name:
            return s["code"]
    return None


def lookup_card(name: str, set_name: str) -> Card:
    logging_msg = f"Attempting to lookup [[{name}]]"
    if set_name:
        logging_msg += f" from {set_name}"
    logger.info(logging_msg)
    # Load DB connection
    db = init_db()

    # Check if card already exists in the DB
    cards = crud.card.get_by_name_set(db=db, name=name, set_name=set_name)
    if len(cards) == 1:
        return cards[0]

    # Not in DB as is, look up the card using fuzzy search from scryfall
    SCRYFALL_FUZZY_SEARCH_ENDPOINT = "https://api.scryfall.com/cards/named?fuzzy="
    if name == "" or name is None:
        logger.info("No card name was provided to look up")
        return None

    query = SCRYFALL_FUZZY_SEARCH_ENDPOINT + name
    if set_name:
        if len(set_name) > 5:
            set_code = lookup_set_code(set_name)
            if set_code is None:
                logger.info(f"Could not find set code for {set_name}")
            query += f"&set={set_code}"
        else:
            query += f"&set={set_name}"
    card_data = requests.get(query).json()
    if card_data["object"] == "error":
        logger.info(f"Error looking up card from scryfall: {card_data['details']}")
        return None
    elif card_data["object"] != "card":
        logger.info("Something went wrong looking up the card on scryfall")
        return None

    # Check to see if the proper card/set name exists in DB
    cards = crud.card.get_by_name_set(
        db=db, name=card_data["name"], set_name=card_data["set_name"]
    )
    if len(cards) == 1:
        return cards[0]

    # This means it's definitely not in DB, so add it

    # Change values to match DB
    card_data["scryfall_id"] = card_data["id"]
    card_data["set_shortname"] = card_data["set"]
    card_data.pop("id", None)
    card_data.pop("set", None)

    card_in = CardCreate(**card_data)
    card = crud.card.create(db=db, obj_in=card_in)
    if not card:
        logger.info("Something went wrong creating the card object from scryfall")
        return None

    return card
