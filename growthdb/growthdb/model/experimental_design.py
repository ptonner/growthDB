from __future__ import unicode_literals

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column,Integer, Unicode,ForeignKey, UnicodeText, UniqueConstraint
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from growthdb.model.strain import Strain
from growthdb.model import DeclarativeBase, metadata, DBSession

class ProxiedDictMixin(object):
    """Adds obj[key] access to a mapped class.

    This class basically proxies dictionary access to an attribute
    called ``_proxied``.  The class which inherits this class
    should have an attribute called ``_proxied`` which points to a dictionary.

    """

    def __len__(self):
        return len(self._proxied)

    def __iter__(self):
        return iter(self._proxied)

    def __getitem__(self, key):
        return self._proxied[key]

    def __contains__(self, key):
        return key in self._proxied

    def __setitem__(self, key, value):
        self._proxied[key] = value

    def __delitem__(self, key):
        del self._proxied[key]

association_table = Table('experimental_design_association', DeclarativeBase.metadata,
    Column('experimental_design_element_id', Integer, ForeignKey('experimental_design_element.id')),
    Column('experimental_design_id', Integer, ForeignKey('experimental_design.id')),
    # Column('right_id', Integer, ForeignKey('right.id'))
)

class ExperimentalDesign_element(DeclarativeBase):
    """An experimental design element."""

    __tablename__ = 'experimental_design_element'

    id = Column(Integer, primary_key=True)
    key = Column(UnicodeText)
    value = Column(UnicodeText)

    experimental_designs = relationship("ExperimentalDesign",
                    secondary=association_table,
                    backref="experimental_design_elements")

    def __repr__(self):
        return "%r:%r" % (self.key,self.value)


# class ExperimentalDesign(ProxiedDictMixin, DeclarativeBase):
class ExperimentalDesign(DeclarativeBase):
    """an experimental design"""

    __tablename__ = 'experimental_design'

    id = Column(Integer, primary_key=True)

    strain_id = Column(Integer, ForeignKey('strain.id'))
    strain = relationship("Strain", backref=backref('experimental_designs', order_by=id))

    # experimental_design_elements = relationship("ExperimentalDesign_element",
    # 			backref="experimental_designs")
                # collection_class=attribute_mapped_collection('key'))

    # _proxied = association_proxy("experimental_design_elements", "value",
    #                     creator=
    #                     lambda key, value: ExperimentalDesign_element(key=key, value=value))

    # def __init__(self, strain):
    #     self.strain = strain

    def __repr__(self):
        return "ExperimentalDesign(%r,%r)" % (self.strain,self.experimental_design_elements)

    def numWells(self):
        return len(self.wells)

    @classmethod
    def with_characteristic(self, key, value):
        return self.experimental_design_element.any(key=key, value=value)
