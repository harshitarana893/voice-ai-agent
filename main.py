from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from google import genai
from google.genai import types

app = FastAPI()

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
    
    # Render na environment variable mathi key lese
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return {"reply": "Error: Render ma GOOGLE_API_KEY ke GEMINI_API_KEY nathi mili rahi."}

    try:
        client = genai.Client(api_key=api_key)
        
        # Gujarati, Hindi, ane English mate Auto Language Detection System Instruction
        system_instruction = (
            "You are a friendly, smart, and natural AI best friend. "
            "Detect the language of the user's input (Gujarati, Hindi, or English). "
            "You MUST always respond in the EXACT SAME language that the user spoke or typed in. "
            "Keep your response warm, engaging, and conversational like a real friend."
        )

        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = "Sorry, mane response apva ma problem thayo."

    return {"reply": ai_reply}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)