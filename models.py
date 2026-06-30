import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    telegram_id = Column(String, unique=True, nullable=True)

class SystemSeasonStatus(Base):
    __tablename__ = "system_season_status"
    
    id = Column(Integer, primary_key=True, index=True)
    is_summer_season = Column(Boolean, default=True)
    well_valve_physically_open = Column(Boolean, default=False)
    last_checked = Column(DateTime, default=datetime.datetime.utcnow)

class WateringHistory(Base):
    __tablename__ = "watering_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    watered_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User")
