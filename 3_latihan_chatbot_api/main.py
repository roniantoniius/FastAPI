import os
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq

from fastapi import FastAPI, HTTPException

# env
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

# inisiasi si fastapi
app = FastAPI(
    title="Biolo-Q 🧬: Marine Biologist Chatbot API",
    version="1.207",
    description="A simple API Langchain Server using Groq ⚡."
)

# template
initial_template = ("Your name is Biolo-Q, Biolo-Q is a marine biologist with 10 years of experience. Biolo-Q will answer all questions related to marine biology with good explanation. If the question is not related to your field, no matter what, just answer with 'Thank you, but it's not my field'.")

# class for input question using pydantic
class QuestionRequest(BaseModel):
    question: str

# this is the method post to send quesstion and get answer
@app.post("/answer")
async def generate_answer(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    final_prompt = f"{initial_template} {question}"

    try:
        # new instance of groq for each request
        groq_chat = ChatGroq(
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama3-8b-8192"
        )

        # groq answer the Q by combining template and question
        response = groq_chat.invoke(final_prompt)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET endpoint to return API information
@app.get("/")
async def get_info():
    return {
        "name": "Biolo-Q 🧬: Marine Biologist Chatbot API",
        "version": "1.207",
        "description": "A simple API Langchain Server using Groq ⚡."
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
