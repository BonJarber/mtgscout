from sqlalchemy.orm import Session

from app import crud
from app.schemas.store import StoreCreate, StoreUpdate
from app.tests.utils.store import create_random_store
from app.tests.utils.utils import random_lower_string, random_url


def test_create_store(db: Session) -> None:
    # Define values
    name = random_lower_string()
    affiliate_code = random_lower_string()
    website = random_url()

    # Build create schema
    store_in = StoreCreate(name=name, affiliate_code=affiliate_code, website=website,)
    # Create store
    store = crud.store.create(db=db, obj_in=store_in)

    # Check values
    assert store.name == name
    assert store.affiliate_code == affiliate_code
    assert store.website == website

    # Clean-up
    crud.store.remove(db=db, id=store.id)


def test_get_store(db: Session) -> None:
    # Create store
    store = create_random_store(db=db)

    # Query created store
    stored_store = crud.store.get(db=db, id=store.id)

    # Check values
    assert stored_store
    assert store.id == stored_store.id
    assert store.name == stored_store.name
    assert store.affiliate_code == stored_store.affiliate_code
    assert store.website == stored_store.website

    # Clean-up
    crud.store.remove(db=db, id=store.id)


def test_update_store(db: Session) -> None:
    # Define values
    name = random_lower_string()
    affiliate_code = random_lower_string()
    website = random_url()

    # Build create schema
    store_in = StoreCreate(name=name, affiliate_code=affiliate_code, website=website,)
    # Create store
    store = crud.store.create(db=db, obj_in=store_in)

    # Define new name
    new_name = random_lower_string()

    # Build update schema
    store_update = StoreUpdate(name=new_name)

    # Update store
    store2 = crud.store.update(db=db, db_obj=store, obj_in=store_update)

    # Check values
    assert store.id == store2.id
    assert store.affiliate_code == store2.affiliate_code
    assert store2.name != name
    assert store2.name == new_name

    # Clean-up
    crud.store.remove(db=db, id=store.id)


def test_delete_store(db: Session) -> None:
    # Define values
    name = random_lower_string()
    affiliate_code = random_lower_string()
    website = random_url()

    # Build create schema
    store_in = StoreCreate(name=name, affiliate_code=affiliate_code, website=website,)
    # Create store
    store = crud.store.create(db=db, obj_in=store_in)

    # Delete store
    store2 = crud.store.remove(db=db, id=store.id)

    # Try querying deleted store
    store3 = crud.store.get(db=db, id=store.id)

    assert store3 is None

    # Check values
    assert store2.id == store.id
    assert store.name == name
    assert store.affiliate_code == affiliate_code
    assert store.website == website
