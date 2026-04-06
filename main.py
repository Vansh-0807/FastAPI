from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal 
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description = 'Name of the Patient')]
    city: Annotated[str, Field(..., description = 'City where patient is living')]
    age: Annotated[int, Field(..., description = 'Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description = "Gender of the Patient")]
    height: Annotated[float, Field(..., gt=0, description = "Height of the Patient")]
    weight: Annotated[float, Field(..., gt=0, description = "Weight of the Patient")]
    # bmi: float
    # verdict: str we will not take bmi and verdict because it has to be calculated by using computed field

    @computed_field
    @property
    def bmi (self) -> 'Patient':
        bmi = round(self.weight/(self.height ** 2),2) 
        return bmi 
    
    @computed_field
    @property
    def verdict(self) -> 'str':
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'normal'
        else:
            return 'obese'

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
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get('/sort')
def sort_patients(sort_by: str=Query(..., description = "sort on the basis of height, weight or bmi"), order_by:str=Query('ascending', description = 'sort in ascending or desending order')):
    fields = ['height', 'weight', 'bmi']

    if fields not in sort_by:
        raise HTTPException(status_code=400, detail = "invalid field select from {fields}")
    
    order = ['ascending', 'descending']
    
    if order not in order_by:
        raise HTTPException(status_code=400, detail = 'invalid order, select in between ascending or descending')
    
    data = load_data

    sort_order = True if order_by == 'descending' else False

    sorted_data = sorted(data.values(), key = lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data
