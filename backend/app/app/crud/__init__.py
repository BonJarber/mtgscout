from .crud_item import item
from .crud_user import user
from .crud_card import card
from .crud_store import store
from .crud_card_price import card_price  # noqa
from .crud_scout import scout  # noqa

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
