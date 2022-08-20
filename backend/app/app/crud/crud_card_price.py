from typing import List, Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.card_price import CardPrice
from app.schemas.card_price import CardPriceCreate, CardPriceUpdate


class CRUDCardPrice(CRUDBase[CardPrice, CardPriceCreate, CardPriceUpdate]):
    pass
    # Use this if you need functionality on update, otherwise delete
    """
    def update(
        self,
        db: Session,
        *,
        db_obj: CardPrice,
        obj_in: Union[CardPriceUpdate, Dict[str, Any]]
    ) -> CardPrice:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if field == "example":
                    pass # Do something here       
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    # Use this if you need functionality on creation, otherwise delete
    def create(self, db: Session, *, obj_in: CardPriceCreate) -> CardPrice:
      # Do something on create
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)  # type: ignore
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj
    """


card_price = CRUDCardPrice(CardPrice)
