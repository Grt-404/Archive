from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('patients.json', 'r') as f:
        return json.load(f)

@app.get("/")
def hello():
    return {"message": "patient management system API"}



@app.get('/view')
def view():
    data = load_data()
    return {"patients": data}
    

#using path params 
@app.get('/greet/{name}')
def greet(name: str):
    return {"message": f"Hello, {name}!"}

# now we can use the path fiunction with path functions in fastapi to provide metadata, like title description and example for the path parameter and provides documentation hints, also used for validation rules

# @app.get('/patient/{patient_id}')
# def view_patient(patient_id: str = Path(..., description = 'ID of the function in db', example = 'P001')):
#     data = load_data()
#     if patient_id in data:
#         return {"patient": data[patient_id]}
#     return {"message": "Patient not found"}

# what is the problem in this ??
# the problem is that if we enter a patient id that is not in the data, it will return a message "Patient not found", but it should return a 404 status code instead of 200, to indicate that the resource was not found. we can fix this by raising an HTTPException with status code 404 when the patient is not found.

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description = 'ID of the function in db', example = 'P001')):
    data = load_data()
    if patient_id in data:
        return {"patient": data[patient_id]}
    raise HTTPException(status_code=404, detail="Patient not found")


# query parameter 

# suppose you get a new request, in which you wanna view all the patuents in a specific order, like you wanna read the patients in ascending order about their weight, we will sue query parametere for the same

# and it is optional key value pairs appended in the end
# just like we had PAth function to document and give metatdata to api's using path params here we have Query function to document and give metadata to api's using query params
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description = 'Sort on the basis of weight, height, or bmi'), order: str = Query('asc', description = 'Sort order, either asc or desc')): # sort by is a required query parameter and order is an optional query parameter with default value 'asc'
    valid_feilds = ['weight', 'height', 'bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400, detail=f"Invalid sort field. select from {valid_feilds}")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid sort order. select from ['asc', 'desc']")
    data = load_data()

    sorted_patients = sorted(data.values(), key=lambda x: x[sort_by], reverse=(order == 'desc'))
    return {"sorted_patients": sorted_patients}