@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_text = data.get("message", "")
    
    # 1. Environment Variable માંથી લેવાનો પ્રયત્ન
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    # 2. જો Render માંથી ના મળે તો અહીં તમારી API Key ડાયરેક્ટ મૂકી દો (Testing માટે)
    if not api_key:
        api_key = "તમારી_અહીંયા_GEMINI_API_KEY_લખો" # અહીં AIzaSy... વાળી Key પેસ્ટ કરો

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
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"API Error: {str(e)}"

    return {"reply": ai_reply}