from sqlalchemy import Column,Integer,String
from Database import Base
class UploadedFile(Base):
	__tablename__="fast_api_uploads"
	id=Column(Integer,primary_key=True,autoincrement=True)
	filename=Column(String,nullable=False)
	content_type=Column(String,nullable=False)
