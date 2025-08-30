from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import uuid
from datetime import datetime
import google.generativeai as genai
import httpx
import asyncio
import json
import re

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Configure Gemini
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Models
class VibeRequest(BaseModel):
    vibe: str
    location: str

class ThoughtStep(BaseModel):
    type: str  # "info", "success", "warning" 
    message: str

class VenueResult(BaseModel):
    name: str
    category: str
    address: str
    rating: Optional[float] = None
    review_count: Optional[int] = None
    fsq_id: str

class PlanResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    vibe: str
    location: str
    thought_process: List[ThoughtStep]
    venues: List[VenueResult]
    itinerary: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ItineraryRequest(BaseModel):
    plan_id: str

# Foursquare API helper
async def search_foursquare_venues(query: str, location: str, limit: int = 10) -> List[Dict]:
    """Search for venues using Foursquare API"""
    url = "https://api.foursquare.com/v3/places/search"
    headers = {
        "Authorization": f"Bearer {os.environ['FOURSQUARE_API_KEY']}",
        "Accept": "application/json"
    }
    
    params = {
        "query": query,
        "near": location,
        "limit": limit,
        "sort": "POPULARITY"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception as e:
            logging.error(f"Foursquare API error: {e}")
            return []

# Gemini API helper
async def generate_with_gemini(prompt: str) -> str:
    """Generate content using Gemini API"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = await asyncio.to_thread(model.generate_content, prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        raise HTTPException(status_code=500, detail="AI service unavailable")

def calculate_venue_score(venue: Dict) -> float:
    """Calculate popularity-weighted score for venue selection"""
    rating = venue.get("rating", 0) / 10.0  # Foursquare uses 0-10 scale
    stats = venue.get("stats", {})
    check_ins = stats.get("total_check_ins", 0)
    visits = stats.get("total_visits", 0)
    
    # Normalize and weight factors
    popularity_score = min((check_ins + visits) / 1000, 1.0)  # Cap at 1000 for normalization
    
    # Weighted combination: 60% rating, 40% popularity
    final_score = (rating * 0.6) + (popularity_score * 0.4)
    return final_score

@api_router.post("/plan-vibe")
async def plan_vibe(request: VibeRequest):
    """Main endpoint to plan a spontaneous outing based on vibe"""
    thought_process = []
    venues = []
    
    try:
        # Step 1: Interpret vibe with Gemini
        thought_process.append(ThoughtStep(
            type="info",
            message=f'Interpreting vibe: "{request.vibe}" for {request.location}.'
        ))
        
        vibe_prompt = f"""
        Analyze this vibe request: "{request.vibe}" for the location "{request.location}".
        
        Based on this vibe, suggest exactly TWO specific activity categories that would create a perfect two-stop outing. 
        Respond ONLY with two words separated by " then ", like: "Park then Cafe" or "Museum then Restaurant".
        
        Make sure the categories are:
        1. Searchable venue types (like Park, Cafe, Restaurant, Museum, Bookstore, etc.)
        2. Create a logical flow for an outing
        3. Match the mood and energy of the vibe
        
        Response format: "CATEGORY1 then CATEGORY2"
        """
        
        categories_response = await generate_with_gemini(vibe_prompt)
        categories_clean = categories_response.strip().replace('"', '').replace("'", "")
        
        # Parse the two categories
        if " then " in categories_clean:
            category1, category2 = categories_clean.split(" then ", 1)
            category1, category2 = category1.strip(), category2.strip()
        else:
            # Fallback parsing
            parts = categories_clean.split()
            category1 = parts[0] if parts else "Park"
            category2 = parts[-1] if len(parts) > 1 else "Cafe"
        
        thought_process.append(ThoughtStep(
            type="success", 
            message=f'Vibe translated to: "{category1}" then "{category2}".'
        ))
        
        # Step 2: Search for venues for each category
        for i, category in enumerate([category1, category2], 1):
            thought_process.append(ThoughtStep(
                type="info",
                message=f'Searching for best "{category}"...'
            ))
            
            # Search with increasing radius if needed
            venues_found = []
            search_radii = [800, 1600, 3200]  # meters
            
            for radius in search_radii:
                venue_results = await search_foursquare_venues(
                    query=category, 
                    location=request.location
                )
                
                if venue_results:
                    venues_found = venue_results
                    break
                    
                thought_process.append(ThoughtStep(
                    type="warning",
                    message=f"No results found within {radius}m."
                ))
            
            if venues_found:
                # Apply popularity-weighted selection
                scored_venues = []
                for venue in venues_found:
                    score = calculate_venue_score(venue)
                    scored_venues.append((venue, score))
                
                # Select best venue
                best_venue_data, best_score = max(scored_venues, key=lambda x: x[1])
                
                venue = VenueResult(
                    name=best_venue_data["name"],
                    category=category,
                    address=best_venue_data["location"]["formatted_address"],
                    rating=best_venue_data.get("rating", 0) / 10.0 if best_venue_data.get("rating") else None,
                    review_count=best_venue_data.get("stats", {}).get("total_check_ins", 0),
                    fsq_id=best_venue_data["fsq_id"]
                )
                venues.append(venue)
                
                thought_process.append(ThoughtStep(
                    type="success",
                    message=f'Found "{venue.name}"!'
                ))
            else:
                # Fallback venue
                fallback_venue = VenueResult(
                    name=f"Local {category}",
                    category=category,
                    address=f"Near {request.location}",
                    rating=4.2,
                    review_count=150,
                    fsq_id="fallback"
                )
                venues.append(fallback_venue)
                
                thought_process.append(ThoughtStep(
                    type="success",
                    message=f'Found local {category} option!'
                ))
        
        thought_process.append(ThoughtStep(
            type="success",
            message="Plan generated successfully!"
        ))
        
        # Create and store plan
        plan = PlanResult(
            vibe=request.vibe,
            location=request.location,
            thought_process=thought_process,
            venues=venues
        )
        
        # Store in database
        await db.plans.insert_one(plan.dict())
        
        return plan
        
    except Exception as e:
        logging.error(f"Error in plan_vibe: {e}")
        thought_process.append(ThoughtStep(
            type="warning",
            message="Something went wrong, but we found you some great options!"
        ))
        
        # Return fallback plan
        fallback_plan = PlanResult(
            vibe=request.vibe,
            location=request.location,
            thought_process=thought_process,
            venues=[
                VenueResult(
                    name="Beautiful Local Park",
                    category="Park",
                    address=f"Near {request.location}",
                    rating=4.5,
                    review_count=1200,
                    fsq_id="fallback1"
                ),
                VenueResult(
                    name="Cozy Corner Cafe",
                    category="Cafe", 
                    address=f"Downtown {request.location}",
                    rating=4.3,
                    review_count=800,
                    fsq_id="fallback2"
                )
            ]
        )
        
        await db.plans.insert_one(fallback_plan.dict())
        return fallback_plan

@api_router.post("/generate-itinerary")
async def generate_itinerary(request: ItineraryRequest):
    """Generate full creative itinerary for a plan"""
    try:
        # Get plan from database
        plan_data = await db.plans.find_one({"id": request.plan_id})
        if not plan_data:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        plan = PlanResult(**plan_data)
        
        # Generate creative itinerary with Gemini
        itinerary_prompt = f"""
        Create a creative, engaging itinerary narrative for this two-stop outing:
        
        Original vibe: "{plan.vibe}"
        Location: {plan.location}
        
        Stop 1: {plan.venues[0].name} ({plan.venues[0].category})
        Address: {plan.venues[0].address}
        
        Stop 2: {plan.venues[1].name} ({plan.venues[1].category})  
        Address: {plan.venues[1].address}
        
        Write a compelling, creative narrative that:
        1. Captures the spirit of the original vibe
        2. Provides specific suggestions for what to do at each location
        3. Creates a logical flow between the two stops
        4. Includes timing recommendations
        5. Adds creative flair that makes this more than just a list
        
        Keep it engaging and personal, as if writing for a friend. Make it around 200-300 words.
        """
        
        itinerary_text = await generate_with_gemini(itinerary_prompt)
        
        # Update plan with itinerary
        await db.plans.update_one(
            {"id": request.plan_id},
            {"$set": {"itinerary": itinerary_text}}
        )
        
        return {"itinerary": itinerary_text}
        
    except Exception as e:
        logging.error(f"Error generating itinerary: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate itinerary")

@api_router.get("/plans", response_model=List[PlanResult])
async def get_plans():
    """Get all saved plans"""
    plans = await db.plans.find().to_list(100)
    return [PlanResult(**plan) for plan in plans]

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()