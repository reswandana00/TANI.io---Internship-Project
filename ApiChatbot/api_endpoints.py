"""
FastAPI REST API for Chatbot Communication.
This API exposes the chatbot functionality as RESTful endpoints.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

# Import chatbot function
from utils import get_chat_response

# Create FastAPI app
app = FastAPI(
    title="Agricultural Chatbot API",
    description="REST API for interacting with the agricultural chatbot",
    version="1.0.0"
)

# Add CORS middleware with comprehensive origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8013",
        "http://10.11.1.207:8013",
        "http://localhost:3000",
        "http://10.11.1.207:3000",
        "http://localhost",
        "http://10.11.1.207",
        "https://10.11.1.207",
        "http://127.0.0.1:8013",
        "http://127.0.0.1:3000",
        "*"  # Allow all for development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ApiResponse(BaseModel):
    success: bool
    data: Any
    message: Optional[str] = None

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Agricultural Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.post("/api/chat", response_model=ApiResponse)
async def chat(request: ChatRequest):
    """Chat with the agricultural chatbot."""
    try:
        print(f"Received chat request: {request.message}")
        response = get_chat_response(request.message)
        print(f"Generated response: {response[:100]}...")
        return ApiResponse(
            success=True,
            data={"response": response},
            message="Chat response generated successfully"
        )
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Additional endpoint for simple GET requests
@app.get("/api/chat", response_model=ApiResponse)
async def chat_get(message: str):
    """Chat with the agricultural chatbot using GET request."""
    try:
        response = get_chat_response(message)
        return ApiResponse(
            success=True,
            data={"response": response},
            message="Chat response generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# List available endpoints
@app.get("/api/endpoints", response_model=Dict[str, List[Dict[str, str]]])
async def list_endpoints():
    """List all available API endpoints."""
    endpoints = [
        {"method": "GET", "path": "/", "description": "Root endpoint with API information"},
        {"method": "GET", "path": "/health", "description": "Health check endpoint"},
        {"method": "POST", "path": "/api/chat", "description": "Chat with the agricultural chatbot"},
        {"method": "GET", "path": "/api/chat?message=your_message", "description": "Chat with the agricultural chatbot using GET"}
    ]
    
    return {"endpoints": endpoints}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)