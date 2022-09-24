from db.base_class import Base
from sqlalchemy import Column, Float, Integer


class YTrain(Base):
    __tablename__ = "ytrains"
    id = Column(Integer, primary_key=True)
    data = Column(Float)
    month = Column(Integer)
    year = Column(Integer)
