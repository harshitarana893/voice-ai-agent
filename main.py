from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from google import genai

app = FastAPI()

# Tamari API key ahiya direct muki do
client = genai.Client(api_key="TAMARI_ASLI_API_KEY_AHI_PASTE_KARO")

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
        # Model name gemini-2.0-flash kari didhu che
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_text,
        )
        ai_reply = response.text
    except Exception as e:
        # Aa error terminal ma print thase ane frontend par pan jase
        print("ERROR:", str(e))
        ai_reply = "Error: " + str(e)

    return {"reply": ai_reply}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)