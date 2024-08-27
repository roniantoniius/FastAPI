# Next Word Prediction Using LSTM Algorithm

The purpose of this website is to be my playground about implementing FastAPI to several kind of project like this one is a Text Processing that use book textfile data from `https://www.gutenberg.org/ebooks/47626` and with LSTM Algorithm to process and predict several next word. So this simple project able to find any specific word from the book. But the model is so simple that only have ability to remember something, but not that good, its memory good until 12 words, after that they perform really bad. You can see at the screenshow `output.png`

## How to run?

1. Re-run the notebook to get several file like tokenizer and model
2. Virtual environment
```
python -m venv env
```
3. Use that python interpreter and install requirements.txt
```
.\venv\Scripts\activate

pip install -r requirements.txt
```
4. Run
```
uvicorn main:app --reload
```
5. Web
```
http://127.0.0.1:8000/beranda
```

### Documentation