# from Database import SessionLocal
# from emp_data import employee

# def create_emp(data):
# 	db=SessionLocal()
# 	emp= employee(
# 		name=data.name,age=data.age
# 	)
# 	db.add(emp)
# 	db.commit()
# 	db.refresh()
# 	return {"message":"success"}
# def up_emp(emp_id,data):
# 	db=SessionLocal()
# 	emp=db.query(employee).filter_by(employee.id==emp_id).first()
# 	emp.name=data.name
# 	emp.age=data.age
# 	db.commit()
# 	db.close()
# def get_all():
# 	db=SessionLocal()
# 	emp=db.query(employee).all()
# 	res=[]
# 	for i in emp:
# 		res.append({
# 			"id":i.id,
# 			"name":i.name,
# 			"age":i.age
# 		})
# 	db.close()
# 	return res

# def delete_emp(emp_id):
# 	db=SessionLocal()
# 	emp=db.query(employee).get(emp_id)
# 	db.delete(emp)
# 	db.commit()

# def get_all(emp_id):
# 	db=SessionLocal()
# 	emp=db.query(employee).get(emp_id)

# 	return emp

from emp_data import employee
from upload_data import UploadedFile


def create_emp(data, db):

    emp = employee(
        name=data.name,
        age=data.age
    )

    db.add(emp)
    db.commit()
    db.refresh(emp)

    db.close()

    return {
        "message": "Success",
        "id": emp.id
    }


def up_emp(emp_id, data, db):

    emp = db.query(employee).filter_by(
        id=emp_id
    ).first()

    if not emp:
        db.close()
        return {"message": "Employee Not Found"}

    emp.name = data.name
    emp.age = data.age

    db.commit()
    db.close()

    return {"message": "Employee Updated"}


def get_all(db, page=1, limit=10, name=None, min_age=None, max_age=None):

    skip = (page - 1) * limit

    query = db.query(employee)

    if name:
        query = query.filter(employee.name.ilike(f"%{name}%"))

    if min_age is not None:
        query = query.filter(employee.age >= min_age)

    if max_age is not None:
        query = query.filter(employee.age <= max_age)

    total = query.count()
    employees = query.offset(skip).limit(limit).all()

    result = []

    for emp in employees:
        result.append({
            "id": emp.id,
            "name": emp.name,
            "age": emp.age
        })

    db.close()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": result
    }

def get_one(emp_id, db):

    emp = db.query(employee).filter_by(
        id=emp_id
    ).first()

    db.close()

    if not emp:
        return {"message": "Employee Not Found"}

    return {
        "id": emp.id,
        "name": emp.name,
        "age": emp.age
    }


def delete_emp(emp_id, db):

    emp = db.query(employee).filter_by(
        id=emp_id
    ).first()

    if not emp:
        db.close()
        return {"message": "Employee Not Found"}

    db.delete(emp)
    db.commit()
    db.close()

    return {"message": "Employee Deleted"}


def save_upload(filename, content_type, db):

    upload = UploadedFile(
        filename=filename,
        content_type=content_type
    )

    db.add(upload)
    db.commit()
    db.refresh(upload)

    db.close()

    return upload.id

def get_save_upload(db, page=1, limit=10):

    skip = (page - 1) * limit

    total = db.query(UploadedFile).count()
    uploads = db.query(UploadedFile).offset(skip).limit(limit).all()

    result = []

    for upload in uploads:
        result.append({
            "id": upload.id,
            "filename": upload.filename,
            "content_type": upload.content_type
        })

    db.close()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": result
    }



