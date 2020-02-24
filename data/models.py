from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Message(Base):
	__tablename__ = 'messages'

	# Information on where the message is.
	id = Column(Integer, primary_key=True)
	user = Column(Integer, nullable=False)
	channel = Column(Integer, nullable=False)
	server = Column(Integer, nullable=False)

	# Other information.
	datetime = Column(Integer, nullable=False)

	# Classification of the message
	classification = Column(Integer, nullable=False)

	# Information about the message itself.
	content = Column(String, nullable=False)

	def __repr__(self):
		return "<Message(user=%d, message='%s')>" % (self.user, self.content)



class Word(Base):
	__tablename__ = 'words'

	id = Column(Integer, primary_key=True)
	word = Column(String, nullable=False)
	count = Column(String, nullable=False)

	def __repr__(self):
		return "<Word(word='%s')>" % (self.word,)


class ClassCount(Base):
	__tablename__ = 'class_count'
	
	id = Column(Integer, primary_key=True)
	count = Column(Integer, nullable=False)

	def __repr__(self):
		return "<ClassCount(id=%d, count=%d)>" % (self.id, self.count)
