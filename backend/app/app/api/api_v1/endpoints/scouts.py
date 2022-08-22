from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Scout])
def read_scouts(
    *,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve scouts.
    """
    if not crud.user.is_superuser(current_user):
        scouts = crud.scout.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    else:
        scouts = crud.scout.get_multi(db=db, skip=skip, limit=limit)
    return scouts


@router.post("/", response_model=schemas.Scout)
def create_scout(
    *,
    db: Session = Depends(deps.get_db),
    scout_in: schemas.ScoutCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new scout.
    """
    if not crud.user.is_superuser(current_user):
        scout_in.user_id = current_user.id
        raise HTTPException(status_code=400, detail="Not enough permissions")

    scout = crud.scout.create(db=db, obj_in=scout_in)
    return scout


@router.put("/{id}", response_model=schemas.Scout)
def update_scout(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    scout_in: schemas.ScoutUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a scout.
    """
    if crud.user.is_superuser(current_user):
        scout = crud.scout.get(db=db, id=id)
    else:
        scout = crud.scout.get_by_owner(db=db, id=id, owner_id=current_user.id)

    if not scout:
        raise HTTPException(status_code=404, detail="Scout not found")
    scout = crud.scout.update(db=db, db_obj=scout, obj_in=scout_in)
    return scout


@router.get("/{id}", response_model=schemas.Scout)
def read_scout(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get scout by ID.
    """
    if crud.user.is_superuser(current_user):
        scout = crud.scout.get(db=db, id=id)
    else:
        scout = crud.scout.get_by_owner(db=db, id=id, owner_id=current_user.id)
    if not scout:
        raise HTTPException(status_code=404, detail="Scout not found")
    return scout


@router.delete("/{id}", response_model=schemas.Scout)
def delete_scout(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a scout.
    """
    if crud.user.is_superuser(current_user):
        scout = crud.scout.get(db=db, id=id)
    else:
        scout = crud.scout.get_by_owner(db=db, id=id, owner_id=current_user.id)

    if not scout:
        raise HTTPException(status_code=404, detail="Scout not found")
    scout = crud.scout.remove(db=db, id=id)
    return scout
