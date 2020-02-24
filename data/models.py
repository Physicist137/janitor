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

	# Information about the message itself.
	content = Column(String, nullable=False)

	def __repr__(self):
		return "Message(user=%d, message='%s')" % (self.user, self.content)






