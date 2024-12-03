import google.generativeai as genai
from schemas import GeneratedTask
from typing import List
import json

genai.configure(api_key="AIzaSyCrtybUxhJrawAQf-OJe6jvy9w6CWdNZa0")


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
        print('DEU ERR')
        return []
    
generateTasks('Gera um plano de estudos de python')