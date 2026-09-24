from pydantic import BaseModel

class Emp_Cre(BaseModel):
	name:str
	age:int

class Emp_up(BaseModel):
	name:str
	age:int