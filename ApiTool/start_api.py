"""
Starter script for the Agricultural Data Analysis API.
This script runs the API using uvicorn.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api_endpoints:app", host="0.0.0.0", port=8011, reload=True)