from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column, Integer
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from growthdb.model import DeclarativeBase, metadata, DBSession, User

class Project(DeclarativeBase):
    """A project."""

    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText,unique=True)
    description = Column(UnicodeText,unique=True)

    user_id = Column(Integer, ForeignKey('tg_user.user_id'))
    user = relationship("User", backref=backref('projects', order_by=id))


    def __repr__(self):
        return "Project (%r)" % (self.name)