import requests
from bs4 import BeautifulSoup
from urllib.parse import ParseResult

from app.db.session import SessionLocal
from app import crud

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"


def parse_cardkingdom_url(url: ParseResult) -> str:
    directories = url.path.strip("/").split("/")
    if len(directories) != 3:
        return "Your URL seems invalid, double check it"
    if directories[0] != "mtg":
        return "Sorry I only support MTG cards at this time"

    html_text = requests.get(url.geturl(), headers={"user-agent": USER_AGENT}).text
    soup = BeautifulSoup(html_text)

    conditions = soup.find("ul", {"class": "cardTypeList"}).find_all("li")
    if len(conditions) == 0:
        return "There was a problem loading card data"

    default_condition = None
    for condition in conditions:
        if condition["class"][1] == "active":
            default_condition = condition["class"][0]

    card_data = soup.find("li", {"class": f"itemAddToCart {default_condition} active"})
    card_set, card_name = card_data.find("input", {"name": "name"})["value"].split(": ")

    is_foil = False
    if card_data.find("input", {"name": "model"})["value"] == "mtg_foil":
        is_foil = True

    db = SessionLocal()
    potential_cards = crud.card.get_by_name_set(
        db=db, name=card_name, set_name=card_set
    )
    if len(potential_cards) > 1:
        message = "I found multiple possible cards:\n"
        for card in potential_cards:
            message += f"{card.name} - {card.set_name} #{card.scryfall_id}"
        return message
    elif len(potential_cards) == 0:
        return f"I couldn't find the card {card_name} from {card_set}"
    card = potential_cards[0]
    message = "I found the card!"
    message += f"{card.name} - {card.set_name} #{card.scryfall_id}"
    return message

