"""
FastAPI REST API for Agricultural Data Analysis Tools.
This API exposes all database tools as RESTful endpoints.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import pandas as pd
import json

# Import all utility functions
from utils import (
    get_data_nasional,
    get_parent_data,
    get_data_panen,
    get_total_data_panen,
    get_wilayah_panen_tertinggi,
    get_wilayah_efektifitas_alsintan,
    get_prompt_ringkasan_data_panen,
    get_data_iklim,
    get_data_ksa,
    chart_one,
    chart_two,
    chart_three,
    chart_four,
    chart_five
)

# Create FastAPI app
app = FastAPI(
    title="Agricultural Data Analysis API",
    description="REST API for accessing Indonesian agricultural data and analysis tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class RegionRequest(BaseModel):
    region: str

class ClimateRequest(BaseModel):
    region: str
    month: Optional[str] = "September"

class ApiResponse(BaseModel):
    success: bool
    data: Any
    message: Optional[str] = None

# Utility function to convert DataFrame to JSON-serializable format
def df_to_json(df):
    """Convert DataFrame to JSON-serializable format."""
    if df is None or df.empty:
        return []
    
    # Replace NaN values with None for JSON serialization
    df_cleaned = df.where(pd.notnull(df), None)
    return df_cleaned.to_dict(orient='records')

# API Endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Agricultural Data Analysis API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

# 1. National Data Endpoint
@app.get("/api/data/nasional", response_model=ApiResponse)
async def api_get_data_nasional():
    """Get national level agricultural data."""
    try:
        df = get_data_nasional()
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message="National data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. Parent Data Endpoint
@app.get("/api/data/parent", response_model=ApiResponse)
@app.post("/api/data/parent", response_model=ApiResponse)
async def api_get_parent_data(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get parent data information for a given region."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        result = get_parent_data(input_region)
        return ApiResponse(
            success=True,
            data=result,
            message="Parent data retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. Agricultural Data by Region
@app.get("/api/data/panen", response_model=ApiResponse)
@app.post("/api/data/panen", response_model=ApiResponse)
async def api_get_data_panen(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get agricultural data based on region input."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_data_panen(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Agricultural data for {input_region} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. Total Agricultural Data
@app.get("/api/data/total-panen", response_model=ApiResponse)
@app.post("/api/data/total-panen", response_model=ApiResponse)
async def api_get_total_data_panen(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get total agricultural data based on region input."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_total_data_panen(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Total agricultural data for {input_region} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. Highest Harvest Regions
@app.get("/api/data/wilayah-panen-tertinggi", response_model=ApiResponse)
@app.post("/api/data/wilayah-panen-tertinggi", response_model=ApiResponse)
async def api_get_wilayah_panen_tertinggi(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get regions with highest harvest data."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_wilayah_panen_tertinggi(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Highest harvest regions for {input_region} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. Agricultural Machinery Effectiveness
@app.get("/api/data/efektifitas-alsintan", response_model=ApiResponse)
@app.post("/api/data/efektifitas-alsintan", response_model=ApiResponse)
async def api_get_wilayah_efektifitas_alsintan(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get regions with highest agricultural machinery effectiveness."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_wilayah_efektifitas_alsintan(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Agricultural machinery effectiveness for {input_region} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. Summary Report
@app.get("/api/data/ringkasan", response_model=ApiResponse)
@app.post("/api/data/ringkasan", response_model=ApiResponse)
async def api_get_prompt_ringkasan_data_panen(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate a summary report for agricultural data."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        summary = get_prompt_ringkasan_data_panen(input_region)
        return ApiResponse(
            success=True,
            data={"summary": summary},
            message=f"Summary report for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. Climate Data
@app.get("/api/data/iklim", response_model=ApiResponse)
@app.post("/api/data/iklim", response_model=ApiResponse)
async def api_get_data_iklim(request: Optional[ClimateRequest] = None, region: str = Query(default="indonesia"), month: str = Query(default="September")):
    """Get climate data based on region and month."""
    try:
        if request:
            input_region = request.region
            input_month = request.month
        else:
            input_region = region
            input_month = month
        
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_data_iklim(input_region, input_month)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Climate data for {input_region} in {input_month} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. KSA Data
@app.get("/api/data/ksa", response_model=ApiResponse)
@app.post("/api/data/ksa", response_model=ApiResponse)
async def api_get_data_ksa(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Get KSA (agricultural statistics) data based on region."""
    try:
        input_region = request.region if request else region
        if not input_region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
        
        df = get_data_ksa(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"KSA data for {input_region} retrieved successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Chart Endpoints
# 10. Chart One - Climate Visualization
@app.get("/api/charts/climate")
@app.post("/api/charts/climate", response_model=ApiResponse)
async def api_chart_one(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate chart data for climate visualization."""
    try:
        input_region = request.region if request else region
        df = chart_one(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Climate chart data for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 11. Chart Two - Harvest Regions
@app.get("/api/charts/harvest-regions")
@app.post("/api/charts/harvest-regions", response_model=ApiResponse)
async def api_chart_two(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate chart data for harvest regions visualization."""
    try:
        input_region = request.region if request else region
        df = chart_two(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Harvest regions chart data for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 12. Chart Three - Harvest vs KSA Comparison
@app.get("/api/charts/harvest-vs-ksa")
@app.post("/api/charts/harvest-vs-ksa", response_model=ApiResponse)
async def api_chart_three(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate chart data for harvest vs KSA comparison."""
    try:
        input_region = request.region if request else region
        df_panen, df_ksa = chart_three(input_region)
        return ApiResponse(
            success=True,
            data={
                "harvest_data": df_to_json(df_panen),
                "ksa_data": df_to_json(df_ksa)
            },
            message=f"Harvest vs KSA comparison data for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 13. Chart Four - Agricultural Machinery Effectiveness
@app.get("/api/charts/machinery-effectiveness")
@app.post("/api/charts/machinery-effectiveness", response_model=ApiResponse)
async def api_chart_four(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate chart data for agricultural machinery effectiveness."""
    try:
        input_region = request.region if request else region
        df = chart_four(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"Machinery effectiveness chart data for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 14. Chart Five - General Agricultural Data
@app.get("/api/charts/general-data")
@app.post("/api/charts/general-data", response_model=ApiResponse)
async def api_chart_five(request: Optional[RegionRequest] = None, region: str = Query(default="indonesia")):
    """Generate chart data for general agricultural data."""
    try:
        input_region = request.region if request else region
        df = chart_five(input_region)
        return ApiResponse(
            success=True,
            data=df_to_json(df),
            message=f"General agricultural chart data for {input_region} generated successfully"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Additional utility endpoints
@app.get("/api/endpoints", response_model=Dict[str, List[Dict[str, str]]])
async def list_endpoints():
    """List all available API endpoints."""
    endpoints = [
        {"method": "GET", "path": "/", "description": "Root endpoint with API information"},
        {"method": "GET", "path": "/health", "description": "Health check endpoint"},
        {"method": "GET", "path": "/api/data/nasional", "description": "Get national level agricultural data"},
        {"method": "POST", "path": "/api/data/parent", "description": "Get parent data information for a region"},
        {"method": "POST", "path": "/api/data/panen", "description": "Get agricultural data by region"},
        {"method": "POST", "path": "/api/data/total-panen", "description": "Get total agricultural data by region"},
        {"method": "POST", "path": "/api/data/wilayah-panen-tertinggi", "description": "Get regions with highest harvest"},
        {"method": "POST", "path": "/api/data/efektifitas-alsintan", "description": "Get agricultural machinery effectiveness"},
        {"method": "POST", "path": "/api/data/ringkasan", "description": "Generate summary report"},
        {"method": "POST", "path": "/api/data/iklim", "description": "Get climate data"},
        {"method": "POST", "path": "/api/data/ksa", "description": "Get KSA data"},
        {"method": "GET/POST", "path": "/api/charts/climate", "description": "Climate visualization data"},
        {"method": "GET/POST", "path": "/api/charts/harvest-regions", "description": "Harvest regions visualization data"},
        {"method": "GET/POST", "path": "/api/charts/harvest-vs-ksa", "description": "Harvest vs KSA comparison data"},
        {"method": "GET/POST", "path": "/api/charts/machinery-effectiveness", "description": "Machinery effectiveness data"},
        {"method": "GET/POST", "path": "/api/charts/general-data", "description": "General agricultural data"},
    ]
    
    return {"endpoints": endpoints}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)