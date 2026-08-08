from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from google import genai

app = FastAPI()

# Render na environment variable mathi API key lese (GOOGLE_API_KEY ke GEMINI_API_KEY banne mathi je male e)
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.get("/")
async def get_index():
    return HTMLResponse(open("index.html", encoding="utf-8").read())

@app.get("/voice")
async def get_voice():
    return HTMLResponse(open("voice.html", encoding="utf-8").read())

@app.get("/static/{file_name}")
async def get_static(file_name: str):
    return FileResponse(f"static/{file_name}")

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_text = data.get("message", "")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_text,
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = "Sorry, mane response apva ma problem thayo."

    return {"reply": ai_reply}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)