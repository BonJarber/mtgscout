from datetime import datetime
from decimal import Decimal
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.scout import ScoutType
from app.tests.utils.card import create_card
from app.tests.utils.scout import create_random_scout
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import (
    random_lower_string,
    random_boolean,
    random_integer,
    random_price,
)


def test_create_scout(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "scout_type": ScoutType.price.value,
        "price": float(random_price()),
        "quantity": random_integer(),
        "condition": random_lower_string(),
        "foil": random_boolean(),
        "nonfoil": random_boolean(),
        "card_id": create_card(db=db).id,
        "user_id": create_random_user(db=db).id,
    }
    response = client.post(
        f"{settings.API_V1_STR}/scouts/", headers=superuser_token_headers, json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["scout_type"] == data["scout_type"]
    assert Decimal(content["price"]).quantize(Decimal(".01")) == Decimal(
        data["price"]
    ).quantize(Decimal(".01"))
    assert content["quantity"] == data["quantity"]
    assert content["condition"] == data["condition"]
    assert content["foil"] == data["foil"]
    assert content["nonfoil"] == data["nonfoil"]
    assert content["card_id"] == data["card_id"]
    assert content["user_id"] == data["user_id"]

    crud.scout.remove(db=db, id=content["id"])


def test_read_scout(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    scout = create_random_scout(db=db)
    response = client.get(
        f"{settings.API_V1_STR}/scouts/{scout.id}", headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["scout_type"] == scout.scout_type
    assert Decimal(content["price"]).quantize(Decimal(".01")) == scout.price
    assert content["quantity"] == scout.quantity
    assert content["condition"] == scout.condition
    assert content["foil"] == scout.foil
    assert content["nonfoil"] == scout.nonfoil
    assert content["first_created"] == scout.first_created.isoformat()
    assert content["last_updated"] == scout.last_updated
    assert content["card_id"] == scout.card_id
    assert content["user_id"] == scout.user_id

    crud.scout.remove(db=db, id=scout.id)
    crud.user.remove(db=db, id=scout.user_id)
    crud.card.remove(db=db, id=scout.card_id)


def test_retrieve_scouts(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    scout_1 = create_random_scout(db=db)
    scout_2 = create_random_scout(db=db)

    r = client.get(f"{settings.API_V1_STR}/scouts/", headers=superuser_token_headers)
    all_scouts = r.json()

    assert len(all_scouts) > 1
    for item in all_scouts:
        assert "id" in item

    crud.scout.remove(db=db, id=scout_1.id)
    crud.scout.remove(db=db, id=scout_2.id)
    crud.card.remove(db=db, id=scout_1.card_id)
    crud.card.remove(db=db, id=scout_2.card_id)
    crud.user.remove(db=db, id=scout_1.user_id)
    crud.user.remove(db=db, id=scout_2.user_id)


def test_update_scout(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    scout = create_random_scout(db=db)
    new_price = float(random_price())
    data = {"price": new_price}

    response = client.put(
        f"{settings.API_V1_STR}/scouts/{scout.id}",
        headers=superuser_token_headers,
        json=data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["id"] == scout.id
    assert Decimal(content["price"]) == new_price

    crud.scout.remove(db=db, id=scout.id)
    crud.card.remove(db=db, id=scout.card_id)
    crud.user.remove(db=db, id=scout.user_id)


def test_delete_scout(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    scout = create_random_scout(db=db)
    card_id = scout.card_id
    user_id = scout.user_id

    response = client.delete(
        f"{settings.API_V1_STR}/scouts/{scout.id}", headers=superuser_token_headers,
    )

    deleted_scout = crud.scout.get(db=db, id=scout.id)
    assert response.status_code == 200
    assert deleted_scout is None
    crud.card.remove(db=db, id=card_id)
    crud.user.remove(db=db, id=user_id)
