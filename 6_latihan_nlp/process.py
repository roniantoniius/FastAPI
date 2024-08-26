import re
import numpy as np
import joblib as jb
from tensorflow.python.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


model = load_model('modeling/model6.keras')
token = jb.load('modeling\\tokenizer.sav')

# like input sentence length
len_sequence = 3


# cleaning data or input
def cleaning(teks):
    teks  = re.sub(r'http\S+|www\.\S+', '', teks)
    teks2 = re.sub(r'[^\w\s]|\r|\n|\d["\']', '', teks)
    teks2 = re.sub(r'[\s]+', ' ', teks2)
    return teks2

# clean input for prediction next word
def clean_input(teks):
    teks_strip = teks.strip()
    clean1     = cleaning(teks_strip)
    return clean1


# prediksi next word
def prediksi_kata(teks):

    # last three words
    teks_split = teks.split(' ')[-len_sequence:]

    # convert to numeric sequence using tokenizer
    sekuensial = token.texts_to_sequences([teks_split])

    # make sure each of the length of sequence is same
    # 'is vast' -> [0, 26, 75]
    sekuensial = pad_sequences(sekuensial,
                               maxlen=len_sequence,
                               padding='pre')
    
    # arr
    sekuensial = np.array(sekuensial)

    # predict the next word
    prediksi = np.argmax(model.predict(sekuensial), axis=-1)
    prediksi = prediksi[0]

    # temporary var to store the predicted word
    pred_word = ''

    # get the predicted word
    # search based on value because the key is the word
    word_index = {value: key for key, value in token.word_index.items()}
    pred_word = word_index.get(prediksi, '')
    return pred_word