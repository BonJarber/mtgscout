import requests
from bs4 import BeautifulSoup
from urllib.parse import ParseResult

from app.db.session import SessionLocal
from app.tasks import lookup_card
from app import crud

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"


def parse_cardkingdom_url(url: ParseResult) -> str:
    directories = url.path.strip("/").split("/")
    if len(directories) != 3:
        return "Your URL seems invalid, double check it"
    if directories[0] != "mtg":
        return "Sorry I only support MTG cards at this time"

    html_text = requests.get(url.geturl(), headers={"user-agent": USER_AGENT}).text
    soup = BeautifulSoup(html_text, features="lxml")

    conditions = soup.find("ul", {"class": "cardTypeList"}).find_all("li")
    if len(conditions) == 0:
        return "There was a problem loading card data"

    default_condition = None
    for condition in conditions:
        if len(condition["class"]) < 2:
            continue
        if condition["class"][1] == "active":
            default_condition = condition["class"][0]

    card_data = soup.find("li", {"class": f"itemAddToCart {default_condition} active"})
    card_set, card_name = card_data.find("input", {"name": "name"})["value"].split(": ")

    is_foil = False
    if card_data.find("input", {"name": "model"})["value"] == "mtg_foil":
        is_foil = True

    card = lookup_card(name=card_name, set_name=card_set)
    if not card:
        message = "I failed to look up the card"
    else:
        message = "I found the card!"
        message += f"\n{card.name} from {card.set_name} \n#{card.scryfall_id}"
    return message

