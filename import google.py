import google.generativeai as genai

genai.configure(api_key="AIzaSyBXjJudPqt-Bb9S-Aq7Tap5Vm1JvgHtdL0")  # replace with your real key

print("\nAvailable models in your account:\n")
for m in genai.list_models():
    print(m.name)
