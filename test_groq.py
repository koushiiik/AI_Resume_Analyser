import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from the project directory
load_dotenv('f:\\Engineering\\PROJECTS\\AI Resume Analyser\\AI_Resume_Analyser\\.env')

api_key = os.environ.get("GROQ_API_KEY")
print("API KEY PRESENT:", bool(api_key))

try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a test assistant."},
            {"role": "user", "content": "Test hello"}
        ],
        temperature=0.6,
        max_tokens=50,
    )
    print("SUCCESS")
    print(response.choices[0].message.content)
except Exception as e:
    print("ERROR:")
    print(repr(e))
