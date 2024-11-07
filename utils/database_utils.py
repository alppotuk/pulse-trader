from sqlalchemy import create_engine, Column,Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pulse import Pulse  
from dotenv import load_dotenv
import os

load_dotenv("config/.env")

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PulseModel(Base):
    __tablename__ = "pulses"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    content = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    sentiment_compound = Column(Float, nullable=False)
    sentiment_negative = Column(Float, nullable=False)
    sentiment_positive = Column(Float, nullable=False)
    sentiment_neutral = Column(Float, nullable=False)
    sentiment_str = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

Base.metadata.create_all(bind=engine)

def save_pulse_to_db(pulse):
    """Saves a Pulse object to the database."""
    db_session = SessionLocal()
    try:
        pulse_entry = PulseModel(
            content=pulse.content,
            sentiment_compound=pulse.sentiment['compound'],
            sentiment_negative=pulse.sentiment['negative'],
            sentiment_positive=pulse.sentiment['positive'],
            sentiment_neutral=pulse.sentiment['neutral'],
            sentiment_str=pulse.sentiment['sentiment'],
            company_name=pulse.company_name,
            timestamp=pulse.timestamp
        )
        db_session.add(pulse_entry)
        db_session.commit()
        print(f"Pulse saved for {pulse.company_name} at {pulse.timestamp}")
    except Exception as e:
        db_session.rollback()
        print("Failed to save pulse:", e)
    finally:
        db_session.close()