# FastAPI Framework: Roni Antonius Playground
### FastAPI for me is a backend to provide a fast and reliable data exchange between different systems and applications using like Restful API or GraphQL API.

### How to run each folder?

**Windows**
1. Create a virtual environment (Opsional, but if u already had all the version of package ur okay)
```
python -m venv env
```
   
2. Use the virtual environment and choose the right `Interpreter`.
```
.\env\Scripts\activate
```

3. Select that environment python interpreter

4. Install all required package and its version
```
pip install -r requirements.txt
```

5. Run FastAPI code (code that call `from fastapi import FastAPI`)
- `python main.py`
**or**
- `uvicorn main:app --reload`

6. Access **Swagger UI**: `http://localhost:8000/docs` or **Redoc UI**: `http://localhost:8000/redoc` on your web browser, but choose the right port.
![post](https://github.com/user-attachments/assets/0b8a0f2b-534d-4285-8858-a83ba95c0be8)
