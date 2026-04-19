from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
import pickle
import pandas as pd

#import the ml model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
    
#creating app object
app = FastAPI()

tier_01_cities = ['Mumbai', 'Delhi', 'Banglore', 'Chennai', 'Kolkata', 'Hyderabad', 'Pune']
tier_02_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt = 0, lt = 120, description = 'Age of the user')]
    weight: Annotated[float, Field(..., gt = 0, description = 'Weight of the user')]
    height: Annotated[float, Field(..., gt = 0, lt=2.5, description = 'Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description = 'Annual salary of the user')]
    smoker: Annotated[bool, Field(..., description = 'Is the user smoked?')]
    city: Annotated[str, Field(..., description = 'The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 
                                  'business_owner', 'unemployed', 'private_job'], 
                          Field(..., description = 'Occupation of the user')]
    
    @computed_field
    @property
    def calc_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.calc_bmi > 30:
            return "high"
        elif self.smoker or self.calc_bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_01_cities:
            return 1
        elif self.city in tier_02_cities:
            return 2
        else:
            return 3

@app.post('/predict')
def predict_premium(data:UserInput):
    variable = pd.DataFrame([{
        'age_group' : data.age_group,
        'city_tier' : data.city_tier,
        'occupation' : data.occupation,
        'income_lpa' : data.income_lpa,
        'lifestyle_risk' : data.lifestyle_risk,
        'bmi' : data.calc_bmi
    }])
    prediction = model.predict(variable)[0]
    return JSONResponse(status_code=200, content={'predicted_category' : prediction})