from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
import uvicorn
import os
from google import genai
from google.genai import types

app = FastAPI()

@app.get("/")
async def get_index():
    if os.path.exists("index.html"):
        return HTMLResponse(open("index.html", encoding="utf-8").read())
    return HTMLResponse("<h1>index.html file not found</h1>")

@app.get("/voice")
async def get_voice():
    if os.path.exists("voice.html"):
        return HTMLResponse(open("voice.html", encoding="utf-8").read())
    return HTMLResponse("<h1>voice.html file not found</h1>")

@app.get("/static/{file_name}")
async def get_static(file_name: str):
    file_path = f"static/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_text = data.get("message", "")
    
    # ૧. Render / Environment Variable માંથી API Key શોધશે
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    # ૨. જો Render માંથી API Key ન મળે, તો નીચે ડબલ કોટ્સ (" ") ની અંદર તમારી Gemini API Key મૂકી શકો છો
    FALLBACK_API_KEY = ""  # ઉદાહરણ: "AIzaSy..."

    if not api_key and FALLBACK_API_KEY:
        api_key = FALLBACK_API_KEY

    if not api_key:
        return {"reply": "Error: Render માં GOOGLE_API_KEY કે GEMINI_API_KEY નથી મળી રહી. Render નું Environment સેટઅપ ચેક કરો."}

    try:
        client = genai.Client(api_key=api_key.strip())
        
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
        ai_reply = response.text if response.text else "No response generated."
    except Exception as e:
        ai_reply = f"API Error: {str(e)}"

    return {"reply": ai_reply}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)