from sqlalchemy import Column , String , DateTime , Float
from sqlalchemy.sql import func
import uuid

from backend.src.core.database import get_db_base


base = get_db_base()

# pretty simple db with one table (for now)
class Asset(base):

    __tablename__ = "assets"

    id = Column(String, primary_key=True , default= lambda : str(uuid.uuid4()))
    name = Column(String , index=True)
    category = Column(String)
    value = Column(Float)
    quantity = Column(Float , default = 1.0)
    status = Column(String)
    purchase_date = Column(DateTime , nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


