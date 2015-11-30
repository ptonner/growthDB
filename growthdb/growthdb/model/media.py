from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column, Integer
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from growthdb.model import DeclarativeBase, metadata, DBSession

class Media(DeclarativeBase):
    """A medium."""

    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText,unique=True)

    def __repr__(self):
        return "Media (%r)" % (self.name)