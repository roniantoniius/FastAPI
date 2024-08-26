import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import uvicorn
import joblib as jb
import tensorflow as tf


import re
import numpy as np
import joblib as jb
from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from process import clean_input, prediksi_kata
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form
from keras.models import load_model




app = FastAPI(
    title="Next Word Prediction Using LSTM",
    description="This is a simple application to predict the next word based on the last three words using data from a book 'The Ocean World: Being a Description of the Sea and Its Living Inhabitants.'",
    version="0.8.1"
)

# prepare for frontend simple app
app.mount("/static", StaticFiles(directory="static"), name="static")
template = Jinja2Templates(directory="templates")

# home page
@app.get("/beranda", response_class=HTMLResponse)
async def beranda(request: Request):
    return template.TemplateResponse("indeks.html", {"request": request})

@app.post("/word_pred_json")
async def word_pred_json(Teks: str = Form(...), no_word: int = Form(...)):
    clean_text = clean_input(Teks)
    
    for _ in range(no_word):
        pred_kata = prediksi_kata(clean_text)
        clean_text += ' ' + pred_kata

    # Format response string
    response_text = f'Hasil Prediksi dari {no_word} kata selanjutnya yaitu: {clean_text}'

    # Return the result as JSON
    return JSONResponse(content={"hasil": response_text})

@app.post("/word_pred")
async def word_pred(request: Request, Teks: str = Form(...), no_word: int = Form(...)):
    clean_text = clean_input(Teks)
    
    # '_' mean we dont use this var on loop
    for _ in range(no_word):
        pred_kata = prediksi_kata(clean_text)
        clean_text += ' ' + pred_kata

    print(f'Hasil Prediksi dari {no_word} kata selanjutnya yaitu: {clean_text}')

    # return the result to frontend
    return template.TemplateResponse("indeks.html", {"request": request, "hasil": clean_text})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")