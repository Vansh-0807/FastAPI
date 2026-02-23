from fastapi import FastAPI, Path
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f: #automatically close the file when it is opened
        data = json.load(f)
    return data

@app.get("/") #this is a get request
def hello():
    return {'message':'Patient Management System API'}

@app.get("/about")
def about():
    return {'message' : 'A fully functional API to manage your patient records'}

@app.get('/view')
def view():
     data = load_data()
     return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'ID of the patient in the DB', examples = 'P001')):
    #first load all the data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    return {'error' : 'patient not found'}