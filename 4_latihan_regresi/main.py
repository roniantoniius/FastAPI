import pickle
import joblib
import uvicorn
import numpy as np
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Depends

app = FastAPI(
    title="Gold Price Prediction",
    description="A simple API that predicts the price of gold based on the input features.",
    version="0.1",
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"}
)

model = joblib.load('gld_data_new.pkl')

@app.get("/")
async def root():
    return {
        "info": "Gold API is an API that predicts the price of gold based on the input features."
    }

class InputData(BaseModel):
    SPX: float
    USO: float
    SLV: float
    EUR_USD: float

    @classmethod
    def my_form(
        cls,
        SPX    : float = Form(...),
        USO    : float = Form(...),
        SLV    : float = Form(...),
        EUR_USD: float = Form(...)
    ): # input form parameter
        
        return cls(
            SPX    = SPX,
            USO    = USO,
            SLV    = SLV,
            EUR_USD= EUR_USD
        )
    
# method for input data and predict
@app.post("/prediksi", response_model=dict)
async def Predict(form_data: InputData = Depends(InputData.my_form)):
    try:
        fitur = np.array([form_data.SPX, form_data.USO, form_data.SLV, form_data.EUR_USD]).reshape(1, -1)

        prediksi = model.predict(fitur)
        return {"Prediksi": prediksi[0]}
    
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)