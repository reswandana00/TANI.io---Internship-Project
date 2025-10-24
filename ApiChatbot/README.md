# Agricultural Chatbot API

This API provides an interface for interacting with the Agricultural Chatbot via HTTP endpoints.

## Features

- Chat with the agricultural bot through REST API endpoints
- Supports both GET and POST requests
- Provides health check and documentation endpoints

## API Endpoints

- `GET /`: Root endpoint with API information
- `GET /health`: Health check endpoint
- `POST /api/chat`: Chat with the agricultural chatbot (JSON request)
- `GET /api/chat?message=your_message`: Chat with the agricultural chatbot (query parameter)
- `GET /api/endpoints`: List all available API endpoints

## Running the API

### Using Python directly

1. Install the requirements:

   ```bash
   pip install -r requirements.txt
   ```

2. Run the API:
   ```bash
   python start_api.py
   ```

### Using Docker

1. Build and run the Docker container:
   ```bash
   docker-compose up -d --build
   ```

The API will be available at http://localhost:8012

## API Documentation

Once the API is running, you can access:

- Swagger UI: http://localhost:8012/docs
- ReDoc: http://localhost:8012/redoc

## Example Usage

### POST Request:

```bash
curl -X POST http://localhost:8012/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Bagaimana hasil panen di Jawa Barat?"}'
```

### GET Request:

```bash
curl "http://localhost:8012/api/chat?message=Bagaimana%20hasil%20panen%20di%20Jawa%20Barat%3F"
```
