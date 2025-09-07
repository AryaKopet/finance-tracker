from sqlalchemy import Column, Integer, String, Boolean, Float
from database import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)

    # Settings
    theme = Column(String(20), default="light")            # "light" atau "dark"
    default_month = Column(Integer, nullable=True)
    default_year = Column(Integer, nullable=True)
    notify_low_balance = Column(Boolean, default=False)
    low_balance_threshold = Column(Float, default=0.0)
    weekly_summary = Column(Boolean, default=False)
    export_format = Column(String(10), default="csv")      # csv / xlsx / pdf

    def __repr__(self):
        return f"<User(name={self.name}, email={self.email})>"
