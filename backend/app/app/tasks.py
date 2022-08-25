import logging

from app.db.session import SessionLocal
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
