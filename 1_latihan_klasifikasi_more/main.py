import joblib
import uvicorn
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Form, Depends

model = joblib.load('pipeline_sepsis.pkl')

app = FastAPI(
    title="Infection Sepsis Classification API",
    description="Sepsis Infection sickness classification using Gradient Boost ML model",
    version="2.0"
)

@app.get("/")
async def root():
    return {
        "info": "Discover Life-Saving Predictions: Our Sepsis Classification API empowers you with accurate, data-driven insights to detect and combat sepsis effectively."
    }

# input data that will be on dataframe
class InputData(BaseModel):
    plasma_glucose: float
    blood_work_result_1: float
    blood_pressure: float
    blood_work_result_2: float
    blood_work_result_3: float
    body_mass_index: float
    blood_work_result_4: float
    Age: int
    Insurance: int

    @classmethod
    def my_form(
        cls,
        plasma_glucose     : float = Form(...),
        blood_work_result_1: float = Form(...),
        blood_pressure     : float = Form(...),
        blood_work_result_2: float = Form(...),
        blood_work_result_3: float = Form(...),
        body_mass_index    : float = Form(...),
        blood_work_result_4: float = Form(...),
        Age                : int   = Form(...),
        Insurance          : int   = Form(...)
    ): # input form parameter
        
        return cls(
            plasma_glucose      = plasma_glucose,
            blood_work_result_1 = blood_work_result_1,
            blood_pressure      = blood_pressure,
            blood_work_result_2 = blood_work_result_2,
            blood_work_result_3 = blood_work_result_3,
            body_mass_index     = body_mass_index,
            blood_work_result_4 = blood_work_result_4,
            Age                 = Age,
            Insurance           = Insurance
        )
    
# method for input data and predict
@app.post("/klasifikasi/")
async def Classify(form_data: InputData = Depends(InputData.my_form)):
    try:
        # input data to dataframe
        dataframe = pd.DataFrame(form_data.dict(), index=[0])

        prediksi  = model.predict_proba(dataframe)

        dataframe["prediksi"] = prediksi.argmax(axis=-1)
        mapp = {0: 'Negative', 1: 'Positive'}
        dataframe["prediksi"] = [mapp[x] for x in dataframe["prediksi"]]

        # conf score
        conf_score = prediksi.max(axis=-1)
        dataframe["conf_score"] = f"{round((conf_score[0]*100), 2)}%"

        # output display
        note = "Classification Successful!"
        code = 1
        pred = dataframe.to_dict("records")

        hasil = {"Notification Message": note, "Notification Code": code, "Prediction": pred}
    
    except Exception as err:

        note = "Classification Failed!"
        code = 0
        pred = None
        hasil = {"Error Message": str(err), "Notification Message": note, "Notification Code": code, "Prediction": pred}
    
    return hasil

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)