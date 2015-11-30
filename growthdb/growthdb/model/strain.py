from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column, Integer
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from growthdb.model import DeclarativeBase, metadata, DBSession

class Strain(DeclarativeBase):
    """A strain."""

    __tablename__ = 'strain'

    id = Column(Integer, primary_key=True)
    parent = Column(ForeignKey('strain.id'))
    gene = Column(UnicodeText)

    def __init__(self, gene, parent):
        self.gene = gene
        self.parent = parent

    def __repr__(self):
        return "Strain (%r)" % self.gene