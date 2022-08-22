from typing import List, Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.scout import Scout
from app.schemas.scout import ScoutCreate, ScoutUpdate


class CRUDScout(CRUDBase[Scout, ScoutCreate, ScoutUpdate]):
    def get_by_owner(self, db: Session, *, id: int, owner_id: int) -> Scout:
        return (
            db.query(self.model)
            .filter(Scout.id == id)
            .filter(Scout.user_id == owner_id)
            .all()
        )

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Scout]:
        return (
            db.query(self.model)
            .filter(Scout.user_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # Use this if you need functionality on update, otherwise delete
    """
    def update(
        self,
        db: Session,
        *,
        db_obj: Scout,
        obj_in: Union[ScoutUpdate, Dict[str, Any]]
    ) -> Scout:
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
    
    def create(self, db: Session, *, obj_in: ScoutCreate) -> Scout:
        if account is not paid:
            user = get_user(db=db, id=obj_in["user_id"])
            if len(user.scouts) > 10:
                throw error?
      # Do something on create
      obj_in_data = jsonable_encoder(obj_in)
      db_obj = self.model(**obj_in_data)  # type: ignore
      db.add(db_obj)
      db.commit()
      db.refresh(db_obj)
      return db_obj
    """


scout = CRUDScout(Scout)
