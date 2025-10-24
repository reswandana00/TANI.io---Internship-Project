# Agricultural Data Analysis API - Docker Guide

This directory contains the dockerized version of the Agricultural Data Analysis API.

## Prerequisites

- Docker installed on your system
- Docker Compose installed on your system (recommended)

## Environment Setup

1. Copy the example environment file and adjust as needed:

   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file to match your database configuration:

   ```
   DATABASE_URL=postgresql://username:password@hostname:5432/database_name
   ```

   > **Note for Docker:** If your database is on your host machine, use `host.docker.internal`
   > (Windows/macOS) or your host IP address (Linux) instead of `localhost`.

## Building and Running with Docker Compose

1. Build and start the container:

   ```bash
   docker-compose up -d
   ```

2. Access the API at [http://localhost:8011](http://localhost:8011)

3. View API documentation at [http://localhost:8011/docs](http://localhost:8011/docs)

4. To stop the container:
   ```bash
   docker-compose down
   ```

## Building and Running with Docker (without Docker Compose)

1. Build the Docker image:

   ```bash
   docker build -t agricultural-api .
   ```

2. Run the container:

   ```bash
   docker run -d -p 8011:8011 --env-file .env --name agri-api agricultural-api
   ```

3. Access the API at [http://localhost:8011](http://localhost:8011)

4. To stop the container:
   ```bash
   docker stop agri-api
   docker rm agri-api
   ```

## API Endpoints

The API provides various endpoints for accessing agricultural data:

- **GET /**: Root endpoint with API information
- **GET /health**: Health check endpoint
- **GET /api/data/nasional**: Get national level agricultural data
- **POST /api/data/parent**: Get parent data information for a region
- **POST /api/data/panen**: Get agricultural data by region
- **POST /api/data/total-panen**: Get total agricultural data by region
- **POST /api/data/wilayah-panen-tertinggi**: Get regions with highest harvest
- **POST /api/data/efektifitas-alsintan**: Get agricultural machinery effectiveness
- **POST /api/data/ringkasan**: Generate summary report
- **POST /api/data/iklim**: Get climate data
- **POST /api/data/ksa**: Get KSA data
- **GET/POST /api/charts/\***: Various chart data endpoints

For a complete list of endpoints, visit the API documentation at [http://localhost:8011/docs](http://localhost:8011/docs) after starting the container.
