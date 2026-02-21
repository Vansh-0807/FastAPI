from fastapi import FastAPI

app = FastAPI()

@app.get("/") #this is a get request
def hello():
    return {'message':'Hello World'}

@app.get("/about")
def about():
    return {'message' : 'This is the 2nd code of FastAPI'}