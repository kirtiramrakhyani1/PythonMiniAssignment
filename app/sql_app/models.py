from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime



class Item(Base):
    __tablename__ = "hutracker"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False,  index=True)
    keyName = Column(String(150), nullable=False)    #key
    description = Column(String(200))                #value
    tags = Column(String(150), nullable=False)
    datatypes = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())
    email = Column(String(70), nullable=False)

    def __repr__(self):
        return 'ItemModel(name=%s, price=%s,store_id=%s)' % (self.id ,self.name, self.keyName, self.tags , self.email)
