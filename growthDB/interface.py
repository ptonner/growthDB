from schema import Strain, Batch, ExperimentalDesign, ExperimentalDesign_element, Well, Base
from sqlalchemy import Session, create_engine

class Interface(object):

	def __init__(self,):
		self.engine = create_engine("sqlite://")
	    Base.metadata.create_all(engine)

	    self.session = Session(bind=engine)