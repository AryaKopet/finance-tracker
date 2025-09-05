# models/transaction.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # sama seperti di user.py

class Transaction(Base):
    __tablename__ = "transactions" 

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)  # <— perbaiki: "user.id"
    type = Column(String(20), nullable=False)  # "income" atau "expense"
    amount = Column(Float, nullable=False)
    description = Column(String(255))
    date = Column(DateTime, default=datetime.utcnow)
    proof_file = Column(String(255), nullable=True)  # nama file bukti transfer

    # Relationship ke User (tidak perlu edit user.py; backref akan dibuat otomatis)
    user = relationship("User", backref="transactions")

    def __repr__(self):
        return f"<Transaction(type={self.type}, amount={self.amount})>"