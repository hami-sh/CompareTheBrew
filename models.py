from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import (
    Column, Integer, Float, String, Boolean, Sequence
)


engine = create_engine('sqlite:///:memory:', echo=True)

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    # store = Column(String)
    # brand = Column(String)
    # name = Column(String, primary_key=True)
    # price = Column(String)
    # type = Column(Float)
    # link = Column(String)
    # ml = Column(Integer)
    # percent = Column(String)
    # std_drinks = Column(Integer)
    # numb_items = Column(Integer)
    # efficiency = Column(Float)
    # image = Column(Float)
    # promotion = Column(Boolean)
    # old_price = Column(Float)

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine, autoflush=False)
session = Session()


ed_user = Item(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)

our_user = session.query(Item).filter_by(name='ed').first()
