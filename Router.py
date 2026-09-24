import os
import shutil
from typing import List,Optional
from fastapi import APIRouter,Depends,UploadFile,HTTPException,Query
from controller import create_emp,delete_emp,up_emp,get_one,get_all,save_upload,get_save_upload
from pydantic_Sk import Emp_Cre,Emp_up
from Database import get_db
from sqlalchemy.orm import Session

UPLOAD_DIR="uploads"
os.makedirs(UPLOAD_DIR,exist_ok=True)

r=APIRouter()
@r.post("/emp")
def creat(data:Emp_Cre,db:Session=Depends(get_db)):
	return create_emp(data,db)

@r.get("/emp")
def get_emp_e(page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100),name:Optional[str]=Query(None),min_age:Optional[int]=Query(None,ge=0),max_age:Optional[int]=Query(None,ge=0),db:Session=Depends(get_db)):
	return get_all(db,page,limit,name,min_age,max_age)

@r.get("/emp/{emp_id}")
def get_emp_id(emp_id,db:Session=Depends(get_db)):
	return get_one(emp_id,db)

@r.put("/emp/{emp_id}")
def up_e(emp_id,data:Emp_up,db:Session=Depends(get_db)):
	return up_emp(emp_id,data,db)

@r.delete("/emp/{emp_id}")
def de_emp(emp_id,db:Session=Depends(get_db)):
	return delete_emp(emp_id,db)

ALLOWED_TYPES=("image/jpeg","image/png","image/gif","image/webp","application/pdf")
MAX_FILE_SIZE=5*1024*1024

@r.post("/upload")
def upload(files:List[UploadFile],db:Session=Depends(get_db)):
	results=[]

	for file in files:
		if file.content_type not in ALLOWED_TYPES:
			raise HTTPException(status_code=400,detail=f"{file.filename}: Only image or PDF files are allowed")

		if file.size>MAX_FILE_SIZE:
			raise HTTPException(status_code=400,detail=f"{file.filename}: File size must not exceed 5 MB")

		file_path=os.path.join(UPLOAD_DIR,file.filename)
		with open(file_path,"wb") as buffer:
			shutil.copyfileobj(file.file,buffer)

		save_upload(file.filename,file.content_type,db)

		results.append({
			"filename":file.filename,
			"content_type":file.content_type
		})

	return results

@r.get("/upload")
def get_upload(page:int=Query(1,ge=1),limit:int=Query(10,ge=1,le=100),db:Session=Depends(get_db)):
	return get_save_upload(db,page,limit)