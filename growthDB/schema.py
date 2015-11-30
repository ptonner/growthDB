"""Mapping a vertical table as a dictionary.

This example illustrates accessing and modifying a "vertical" (or
"properties", or pivoted) table via a dict-like interface.  These are tables
that store free-form object properties as rows instead of columns.  For
example, instead of::

  # A regular ("horizontal") table has columns for 'species' and 'size'
  Table('animal', metadata,
        Column('id', Integer, primary_key=True),
        Column('species', Unicode),
        Column('size', Unicode))

A vertical table models this as two tables: one table for the base or parent
entity, and another related table holding key/value pairs::

  Table('animal', metadata,
        Column('id', Integer, primary_key=True))

  # The properties table will have one row for a 'species' value, and
  # another row for the 'size' value.
  Table('properties', metadata
        Column('animal_id', Integer, ForeignKey('animal.id'),
               primary_key=True),
        Column('key', UnicodeText),
        Column('value', UnicodeText))

Because the key/value pairs in a vertical scheme are not fixed in advance,
accessing them like a Python dict can be very convenient.  The example below
can be used with many common vertical schemas as-is or with minor adaptations.

"""
from __future__ import unicode_literals

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


from sqlalchemy import (Column, Integer, Unicode,
    ForeignKey, UnicodeText, and_, create_engine, UniqueConstraint)
from sqlalchemy.orm import relationship, Session, backref
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Strain(Base):
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

class ExperimentalDesign_element(Base):
    """An experimental design element."""

    __tablename__ = 'experimental_design_element'

    ed_id = Column(ForeignKey('experimental_design.id'), primary_key=True)
    key = Column(Unicode(64), primary_key=True)
    value = Column(UnicodeText)

    def __repr__(self):
        return "%r" % (self.value)

class ExperimentalDesign(ProxiedDictMixin, Base):
    """an experimental design"""

    __tablename__ = 'experimental_design'

    id = Column(Integer, primary_key=True)

    strain_id = Column(Integer, ForeignKey('strain.id'))
    strain = relationship("Strain", backref=backref('experimental_designs', order_by=id))

    experimental_design_elements = relationship("ExperimentalDesign_element",
                collection_class=attribute_mapped_collection('key'))

    _proxied = association_proxy("experimental_design_elements", "value",
                        creator=
                        lambda key, value: ExperimentalDesign_element(key=key, value=value))

    def __init__(self, strain):
        self.strain = strain

    def __repr__(self):
        return "ExperimentalDesign(%r,%r)" % (self.strain,self.experimental_design_elements)

    def numWells(self):
        return len(self.wells)

    @classmethod
    def with_characteristic(self, key, value):
        return self.experimental_design_element.any(key=key, value=value)

class Batch(Base):
    """A batch of OD measurements."""

    __tablename__ = 'batch'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "Batch(%r)" % (self.name)

class Well(Base):
    """A well with OD measurements."""

    __tablename__ = 'well'

    id = Column(Integer, primary_key=True)

    batch_id = Column(Integer, ForeignKey('batch.id'))
    batch = relationship("Batch", backref=backref('wells', order_by=id))

    ed_id = Column(Integer, ForeignKey('experimental_design.id'))
    experimental_design = relationship("ExperimentalDesign", backref=backref('wells', order_by=id))

    biorep = Column(Integer,nullable=False)
    techrep = Column(Integer,nullable=False)

    __table_args__ = (
        UniqueConstraint("ed_id","batch_id","biorep", "techrep"),
        )

    def __init__(self,batch,ed,biorep=None,techrep=None):
        self.batch = batch
        self.experimental_design = ed
        self.biorep = biorep
        self.techrep = techrep

    def __repr__(self):
        return "Well(%r, %r, %r, %r)" % (self.batch,self.experimental_design,self.biorep,self.techrep)

if __name__ == '__main__':
    
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    session = Session(bind=engine)

    """Setup strains"""

    nrc1 = Strain("nrc1",None)
    session.add(nrc1)
    session.commit()

    ura3 = Strain("ura3",nrc1.id)
    session.add(ura3)
    session.commit()

    q = session.query(Strain).filter(Strain.id == ura3.parent)
    print 'ura3 parent:', q.all()

    session.add_all([Strain("rosR",ura3.id),
                     Strain("trmB",ura3.id),])
    session.commit()

    q = session.query(Strain)
    print 'Strains:', q.all()


    """Setup experimental designs"""

    ed1 = ExperimentalDesign(ura3)
    ed1['mM PQ'] = "0.333"

    print ed1

    session.add(ed1)
    session.commit()

    ed2 = ExperimentalDesign(ura3)
    ed2['mM PQ'] = "0"

    print ed2

    session.add(ed2)
    session.commit()

    """Add a batch"""
    batch = Batch("test batch")
    session.add(batch)
    session.commit()

    """Add some wells"""
    session.add_all([Well(batch,ed1,i/3,i%3) for i in range(10)])
    session.commit()
    print "\n".join([str(w) for w in session.query(Well).all()])

    q = (session.query(ExperimentalDesign).
         filter(ExperimentalDesign.experimental_design_elements.any(
           and_(ExperimentalDesign_element.key == 'mM PQ',
                ExperimentalDesign_element.value == '0.333'))))
    print 'found wells:', [ed.numWells() for ed in q.all()]

    # q = session.query(Animal).\
    #         filter(Animal.with_characteristic("color", 'brown'))
    # print('brown animals', q.all())

    # q = session.query(Animal).\
    #        filter(~Animal.with_characteristic("poisonous-part", 'elbows'))
    # print('animals without poisonous-part == elbows', q.all())

    # q = (session.query(Animal).
    #      filter(Animal.facts.any(value='somewhat')))
    # print('any animal with any .value of "somewhat"', q.all())
