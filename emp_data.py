from sqlalchemy import Column,Integer,String
from Database import Base
class employee(Base):
	__tablename__="fast_api_emp"
	id=Column(Integer,primary_key=True,autoincrement=True)
	name=Column(String,nullable=False)
	age=Column(Integer,nullable=False)