# DrawHub AI API

A FastAPI application that converts text prompts into Excalidraw code using OpenAI's GPT models.

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Running the Application

Start the server with:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /generate
Convert a text prompt into Excalidraw code.

Request body:
```json
{
    "prompt": "Draw a simple house with a tree"
}
```

Response:
```json
{
    "excalidraw_code": "... Excalidraw JSON code ..."
}
```

### GET /
Welcome message and basic information about the API.

## API Documentation

Once the server is running, you can access:
- Interactive API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`