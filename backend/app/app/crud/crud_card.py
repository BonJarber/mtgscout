from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


class CRUDCard(CRUDBase[Card, CardCreate, CardUpdate]):
    pass


card = CRUDCard(Card)
