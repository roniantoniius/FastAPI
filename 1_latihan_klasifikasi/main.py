import pickle
import uvicorn
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Infection Sepsis Classification API",
    description="Sepsis Infection sickness classification using Gradient Boost ML model",
    version="1.0"
)

# Load model, encoder, and scaler from the pickled file
with open('model_and_key_components_new.pkl', 'rb') as fl:
    komponen = pickle.load(fl)

model_gb = komponen['model']
scaler = komponen['scaler']

# Input data schema
class InputData(BaseModel):
    PRG: int
    PL: float
    PR: float
    SK: float
    TS: int
    M11: float
    BD2: float
    Age: int

@app.get("/")
def read_root():
    return {"message": "Welcome to this fantastic app!"}

# Output data schema
class OutputClass(BaseModel):
    Sepsis: str

# Preprocess input data
def data_preprocess(input_data: InputData):
    input_values = [list(input_data.dict().values())]
    scaled_data = scaler.transform(input_values)
    return pd.DataFrame(scaled_data, columns=input_data.dict().keys())

# Classify the preprocessed data
def classify(scaled_df):
    mapping = {0: 'Negative', 1: 'Positive'}
    y_pred = model_gb.predict(scaled_df)
    return mapping[y_pred[0]]

@app.get("/")
async def root():
    return "Discover Life-Saving Predictions: Our Sepsis Classification API empowers you with accurate, data-driven insights to detect and combat sepsis effectively."

@app.post("/klasifikasi/", response_model=OutputClass)
async def klasifikasi(input_data: InputData):
    try:
        scaled_df = data_preprocess(input_data)
        status = classify(scaled_df)
        return {"Sepsis": status}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))