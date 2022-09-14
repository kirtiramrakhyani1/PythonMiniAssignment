from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from datetime import datetime

class ItemBase(BaseModel):
    name: str
    keyName : str
    description: Optional[str] = None
    tags: str
    datatypes: str
    created_at: datetime
    updated_at: datetime
    email: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class ItemName(ItemBase):
    name: str
#