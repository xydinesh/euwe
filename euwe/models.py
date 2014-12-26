from datetime import datetime

from sqlalchemy import (
    Column,
    Index,
    Integer,
    String,
    DateTime,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# adding authentication and authrization
from pyramid.security import Allow, Everyone

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, "everybody"),
                (Allow, "basic", "entry"),
                (Allow, "secured", ("entry", "topsecret"))
              ]
    def __init__(self, request):
        pass


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)

class PositionModel(Base):
    __tablename__ = 'tbl_positions'
    id = Column(Integer, primary_key=True)
    fen = Column(String(128))
    category = Column(Integer)
    hint = Column(String(128))
    instructions = Column(String(1024))
    solution = Column(Text)
    move = Column(Integer)
    mate_in = Column(Integer)
    pgn = Column(Text)
    created = Column(DateTime)
    modified = Column(DateTime)
    category_key = ''

    categories = {
        'game': 1,
        'problem': 2,
        'position': 3,
        'analysis': 4,
    }

    def __init__(self, category, fen=None, pgn=None):
        self.category_key = category
        if fen:
            self.fen = fen
        if pgn:
            self.pgn = pgn

        self.category = self.categories[category]
        self.created = datetime.utcnow()
        self.modified = datetime.utcnow()

    def __repr__(self):
        return 'Position <{0} {1}>'.format(self.id, self.category_key)
