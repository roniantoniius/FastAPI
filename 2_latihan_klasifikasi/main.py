import pickle
import joblib
import uvicorn
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

app = FastAPI(
    title="Loan-C: Loan or Credit Risk Classifier for lending firm at Bandora"
)

class Pinjaman(BaseModel):
    LanguageCode: object
    HomeOwnershipType: object
    Restructured: object
    IncomeTotal: float
    LiabilitiesTotal: float
    LoanDuration: float
    AppliedAmount: float
    Amount: float
    Interest: float
    EMI: float
    PreviousRepaymentsBeforeLoan: float
    MonthlyPaymentDay: float
    PrincipalPaymentsMade: float
    InterestAndPenaltyPaymentsMade: float
    PrincipalBalance: float
    InterestAndPenaltyBalance: float
    Bids: float
    Rating: object

# will run when the app starts
@app.on_event("startup")
def load_model_RF():
    global RF_model
    RF_model = joblib.load('RFC_pipeline.sav')

# function to classify either defaulted or not
@app.post("/classify")
def classify_loan(data: Pinjaman):

    # data but in pd dataframe
    input_data = {
        "LanguageCode": data.LanguageCode,
        "HomeOwnershipType": data.HomeOwnershipType,
        "Restructured": data.Restructured,
        "IncomeTotal": data.IncomeTotal,
        "LiabilitiesTotal": data.LiabilitiesTotal,
        "LoanDuration": data.LoanDuration,
        "AppliedAmount": data.AppliedAmount,
        "Amount": data.Amount,
        "Interest": data.Interest,
        "EMI": data.EMI,
        "PreviousRepaymentsBeforeLoan": data.PreviousRepaymentsBeforeLoan,
        "MonthlyPaymentDay": data.MonthlyPaymentDay,
        "PrincipalPaymentsMade": data.PrincipalPaymentsMade,
        "InterestAndPenaltyPaymentsMade": data.InterestAndPenaltyPaymentsMade,
        "PrincipalBalance": data.PrincipalBalance,
        "InterestAndPenaltyBalance": data.InterestAndPenaltyBalance,
        "Bids": data.Bids,
        "Rating": data.Rating
    }

    # here is the real dataframe
    input_df = pd.DataFrame(input_data, index=[0])
    # indeks 0 karena hanya satu data terhadap model

    klasifikasi = RF_model.predict(input_df)


    if klasifikasi == 0:
        return {"Classification": "Not Defaulted"}
    else:
        return {"Classification": "Defaulted"}
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
