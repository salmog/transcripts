from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///transcripts_isolated.db') # Local file, no DB port conflict
Session = sessionmaker(bind=engine)

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    channel_url = Column(String, unique=True)
    name = Column(String)

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    video_id = Column(String, unique=True)
    channel_id = Column(Integer, ForeignKey('channels.id'))
    title = Column(String)
    published_at = Column(DateTime)
    transcript = Column(Text)

class TradeSetup(Base):
    __tablename__ = 'trade_setups'
    id = Column(Integer, primary_key=True)
    video_id = Column(String, ForeignKey('videos.video_id'))
    ticker = Column(String) # ENGLISH CAPITAL
    sentiment = Column(String)
    stop_loss = Column(String)
    entry_level = Column(String)
    support = Column(String)
    resistance = Column(String)
    breakout = Column(String)
    retest_bounce = Column(String)
    catalyst_news = Column(Text)
    full_setup_summary = Column(Text)

Base.metadata.create_all(engine)
