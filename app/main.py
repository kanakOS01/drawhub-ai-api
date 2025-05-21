from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import re

from app.prompt import system_message

# Load environment variables
load_dotenv()

app = FastAPI(title="DrawHub AI API")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class PromptRequest(BaseModel):
    prompt: str

class ExcalidrawResponse(BaseModel):
    excalidraw_code: str

def extract_json_from_markdown(text: str) -> str:
    """Extract JSON from markdown code blocks if present."""
    # Look for content between ```json and ``` or between ``` and ```
    json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    match = re.search(json_pattern, text)
    
    if match:
        return match.group(1).strip()
    return text.strip()

@app.post("/generate", response_model=ExcalidrawResponse)
async def generate_excalidraw(request: PromptRequest):
    try:
        # Make the API call to OpenAI
        response = client.chat.completions.create(
            model="gpt-4",  # You can change this to other models if needed
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": request.prompt}
            ],
            temperature=0.7,
        )

        # Extract the generated Excalidraw code
        raw_response = response.choices[0].message.content
        print("Raw response:", raw_response)
        
        # Extract JSON from markdown code blocks if present
        elements_str = extract_json_from_markdown(raw_response)
        print("Extracted elements:", elements_str)
        
        try:
            # Try to parse the elements as JSON
            elements = json.loads(elements_str)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to parse Excalidraw code as JSON: {str(e)}"
            )
        
        # Wrap the elements in the proper Excalidraw structure
        excalidraw_code = {
            "type": "excalidraw/clipboard",
            "elements": elements
        }
        print("Final excalidraw code:", excalidraw_code)

        return ExcalidrawResponse(excalidraw_code=json.dumps(excalidraw_code))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Welcome to DrawHub AI API. Use POST /generate endpoint to convert prompts to Excalidraw code."} 