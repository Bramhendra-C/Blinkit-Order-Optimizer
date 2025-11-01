import math
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # NEW: Import CORS Middleware
from pydantic import BaseModel, Field
from typing import List, Dict, Tuple

# --- Configuration and Constants ---
# Assuming average delivery speed of 30 km/h for calculation
AVG_SPEED_KMH = 30.0
# Earth radius for Haversine calculation (in kilometers)
R_EARTH_KM = 6371.0

# --- Pydantic Data Models ---

class Location(BaseModel):
    """Represents a geographic location."""
    id: str = Field(..., description="Unique ID for the location (e.g., 'store' or 'cust-1').")
    lat: float = Field(..., description="Latitude of the location.")
    lon: float = Field(..., description="Longitude of the location.")

class OrderRequest(BaseModel):
    """Input model for the route optimization request."""
    store_location: Location
    customer_locations: List[Location] = Field(..., description="List of customer drop-off points.")

class RouteSegment(BaseModel):
    """Represents one segment of the optimized route."""
    from_id: str
    to_id: str
    distance_km: float
    time_minutes: float

class RouteResponse(BaseModel):
    """Output model for the optimized route calculation."""
    optimized_route: List[RouteSegment]
    total_time_minutes: float
    total_distance_km: float
    optimal_sequence: List[str]

# --- Core Logic: Geospatial and Algorithm ---

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculates the great-circle distance between two points 
    on the Earth using the Haversine formula (in kilometers).
    """
    # Convert degrees to radians
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance_km = R_EARTH_KM * c
    return distance_km

def calculate_travel_time(distance_km: float) -> float:
    """
    Calculates travel time in minutes based on distance and average speed.
    (Time = Distance / Speed)
    """
    # Time in hours = Distance (km) / Speed (km/h)
    time_hours = distance_km / AVG_SPEED_KMH
    # Time in minutes
    return time_hours * 60

def nearest_neighbor_optimization(
    store: Location, 
    customers: List[Location]
) -> Tuple[List[RouteSegment], float, float, List[str]]:
    """
    Implements a Nearest Neighbor Heuristic to solve the Traveling Salesman Problem (TSP) 
    for finding the sequence of customers that minimizes total travel time.
    """
    if not customers:
        return [], 0.0, 0.0, [store.id]

    all_locations: Dict[str, Location] = {loc.id: loc for loc in [store] + customers}
    unvisited_ids = {cust.id for cust in customers}
    current_location = store

    optimized_route: List[RouteSegment] = []
    optimal_sequence: List[str] = [store.id]
    total_time_minutes = 0.0
    total_distance_km = 0.0

    while unvisited_ids:
        nearest_customer_id = None
        min_time = float('inf')
        
        # Find the nearest unvisited customer
        for next_id in unvisited_ids:
            next_location = all_locations[next_id]
            
            distance = haversine(
                current_location.lat, current_location.lon, 
                next_location.lat, next_location.lon
            )
            time_m = calculate_travel_time(distance)
            
            if time_m < min_time:
                min_time = time_m
                nearest_customer_id = next_id
        
        # Add the segment to the route
        if nearest_customer_id:
            next_location = all_locations[nearest_customer_id]
            
            distance = haversine(
                current_location.lat, current_location.lon, 
                next_location.lat, next_location.lon
            )
            time_m = calculate_travel_time(distance)

            segment = RouteSegment(
                from_id=current_location.id,
                to_id=nearest_customer_id,
                distance_km=distance,
                time_minutes=time_m
            )
            
            optimized_route.append(segment)
            optimal_sequence.append(nearest_customer_id)
            total_time_minutes += time_m
            total_distance_km += distance
            
            # Move to the new location and mark as visited
            current_location = next_location
            unvisited_ids.remove(nearest_customer_id)

    return optimized_route, total_time_minutes, total_distance_km, optimal_sequence

# --- FastAPI Setup ---

app = FastAPI(
    title="Blinkit Order Optimizer API",
    description="Calculates the fastest delivery sequence using Nearest Neighbor Heuristic and Haversine distance."
)

# NEW: CORS Middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "Blinkit Order Optimizer API is running. Use the /optimize_route endpoint."}

@app.post("/optimize_route", response_model=RouteResponse)
async def optimize_route(request: OrderRequest):
    """
    Accepts a store location and a list of customer locations, and returns
    the optimal delivery route sequence and ETA.
    """
    if not request.customer_locations:
        raise HTTPException(status_code=400, detail="At least one customer location is required.")

    try:
        (
            optimized_route, 
            total_time, 
            total_distance, 
            optimal_sequence
        ) = nearest_neighbor_optimization(
            request.store_location, 
            request.customer_locations
        )

        return RouteResponse(
            optimized_route=optimized_route,
            total_time_minutes=total_time,
            total_distance_km=total_distance,
            optimal_sequence=optimal_sequence
        )

    except Exception as e:
        print(f"Error during optimization: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during route calculation.")

# How to run (requires uvicorn to be installed): 
# uvicorn optimizer_api:app --reload
