import google.generativeai as genai

genai.configure(api_key="AIzaSyBXjJudPqt-Bb9S-Aq7Tap5Vm1JvgHtdL0 ")

def ask_gemini(prompt):
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # ✅ updated model
    response = model.generate_content(prompt)
    return response.text




