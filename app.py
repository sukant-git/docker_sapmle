from fastapi import FastAPI
from Router import r
from Database import Base, engine
app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(r)
@app.get("/")
def home():
	return "home"