from sqlalchemy import *
from sqlalchemy.orm import mapper, relation, relationship, Session, backref
from sqlalchemy import Table, ForeignKey, Column, Integer
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.associationproxy import association_proxy

from tgext.datahelpers.fields import Attachment
# from depot.fields.sqlalchemy import UploadedFileField

from growthdb.model import DeclarativeBase, metadata, DBSession, Project

class Plate(DeclarativeBase):
    """A plate."""

    __tablename__ = 'plate'

    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText,unique=True)
    description = Column(UnicodeText,unique=True)
    raw_data = Column(Attachment)
    # raw_data = Column(UploadedFileField)

    project_id = Column(Integer, ForeignKey('project.id'))
    project = relationship("Project", backref=backref('plates', order_by=id))



    def __repr__(self):
        return "Plate (%r)" % (self.name)