import uvicorn
import joblib
import pandas as pd
import numpy as np
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sklearn.preprocessing import MinMaxScaler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Request, Form

app = FastAPI(
    title="Covid-19 API: Predicting Patient Risk 💊.",
    version="3.1"
)

# this will able our app to accept request from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

df      = pd.read_csv("training_csv")
scaler  = MinMaxScaler()
df.drop('Target', axis=1, inplace=True)
df      = scaler.fit_transform(df)
model   = joblib.load("covid-19 model.pkl")

class InputData(BaseModel):
    USMER: int
    MEDICAL_UNIT: int
    SEX: int
    PATIENT_TYPE: int
    INTUBED: int
    AGE: int
    PREGNANT: int
    CLASIFFICATION_FINAL: int
    ICU: int

@app.get("/")
def root(request: Request):
    return template.TemplateResponse("indeks.html", {"request": request})

@app.post("/classify")
def classify(data: InputData):
    try:
        list_fitur = [data.USMER,
                      data.MEDICAL_UNIT,
                      data.SEX,
                      data.PATIENT_TYPE,
                      data.INTUBED,
                      data.AGE,
                      data.PREGNANT,
                      data.CLASIFFICATION_FINAL,
                      data.ICU]

        data_arr = np.array([list_fitur])
        scaled = scaler.transform(data_arr)

        classification = model.predict(scaled)[0]

        result = "Patient In Risk" if int(classification) == 1 else "Patient Not In Risk"

        return {"prediction": result}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred during classification: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
