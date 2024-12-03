import google.generativeai as genai
from schemas import GeneratedTask
import json
import os

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def generateTasks(content: str) -> list:
    try:
        result = model.generate_content(
        content,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=list[GeneratedTask]
        ),
        )
        return json.loads(result.candidates[0].content.parts[0].text)
    except:
        print('Error while getting Gemini response')
        return []