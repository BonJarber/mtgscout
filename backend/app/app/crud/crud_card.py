from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.card import Card
from app.schemas.card import CardCreate, CardUpdate


class CRUDCard(CRUDBase[Card, CardCreate, CardUpdate]):
    def get_by_name_set(self, db: Session, *, name: str, set_name: str) -> List[Card]:
        return (
            db.query(self.model)
            .filter(Card.name == name)
            .filter(Card.set_name == set_name)
            .all()
        )


card = CRUDCard(Card)
