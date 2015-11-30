from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column, Integer, UniqueConstraint
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from growthdb.model import DeclarativeBase, metadata, DBSession, Plate, ExperimentalDesign

class Well(DeclarativeBase):
    """A well with OD measurements."""

    __tablename__ = 'well'

    id = Column(Integer, primary_key=True)
    number = Column(Integer, primary_key=False)

    plate_id = Column(Integer, ForeignKey('plate.id'))
    plate = relationship("Plate", backref=backref('wells', order_by=id))

    ed_id = Column(Integer, ForeignKey('experimental_design.id'))
    experimental_design = relationship("ExperimentalDesign", backref=backref('wells', order_by=id))

    biorep = Column(Integer,nullable=False)
    techrep = Column(Integer,nullable=False)

    __table_args__ = (
        UniqueConstraint("ed_id","plate_id","biorep", "techrep"),
        )

    def __repr__(self):
        return "Well(%r, %r, %r, %r)" % (self.batch,self.experimental_design,self.biorep,self.techrep)
