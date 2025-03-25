from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import time
import requests
from typing import Optional
import asyncio

# Create FastAPI app instance
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Pydantic models for request/response validation
class ImageGenerationRequest(BaseModel):
    prompt: str
    width: Optional[int] = 1440
    height: Optional[int] = 800

class ImageGenerationResponse(BaseModel):
    request_id: str
    status: str

class ImageResultResponse(BaseModel):
    image_url: str
    status: str

def generate_image(prompt: str, width: int = 1440, height: int = 800):
    """Simple function to generate an image from a prompt"""
    API_KEY = "e96c04dc-dfce-4025-9494-225ea940ed92"
    
    try:
        response = requests.post(
            'https://api.bfl.ml/v1/flux-pro-1.1',
            headers={
                'accept': 'application/json',
                'x-key': API_KEY,
                'Content-Type': 'application/json',
            },
            json={
                'prompt': prompt,
                'width': width,
                'height': height,
            },
        )
        
        request = response.json()
        
        if 'id' not in request:
            raise HTTPException(status_code=400, detail="Invalid API response")
            
        return request["id"]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating image: {str(e)}")

def retrieve_image_result(request_id: str):
    """Poll the API until the image generation is complete and return the result URL."""
    API_KEY = "e96c04dc-dfce-4025-9494-225ea940ed92"
    
    try:
        result = requests.get(
            'https://api.bfl.ml/v1/get_result',
            headers={
                'accept': 'application/json',
                'x-key': API_KEY,
            },
            params={
                'id': request_id,
                'width': 1024,
                'height': 1024/2,
            },
        ).json()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving image: {str(e)}")

# Create FastAPI endpoints
@app.post("/generate-image/", response_model=ImageGenerationResponse)
async def create_image(request: ImageGenerationRequest):
    """Endpoint to start image generation"""
    request_id = generate_image(request.prompt, request.width, request.height)
    return ImageGenerationResponse(request_id=request_id, status="processing")

@app.get("/image-result/{request_id}", response_model=ImageResultResponse)
async def get_image_result(request_id: str):
    """Endpoint to get the generated image result"""
    result = retrieve_image_result(request_id)
    
    if result["status"] == "Ready":
        return ImageResultResponse(
            image_url=result['result']['sample'],
            status="completed"
        )
    return ImageResultResponse(
        image_url="",
        status=result["status"]
    )

@app.post("/process_exercise")
async def process_exercise(request: Request):
    try:
        data = await request.json()
        exercise_statement = data.get("exercise_statement")
        
        # Modify the prompt here
        image_prompt = f"""Professional high-quality photorealistic image that represents: 
        {exercise_statement}. 
        The image should be bright, colorful and engaging, suitable for educational purposes.
        Style: Pixar-like 3D animation, cheerful and modern."""
        
        # Generate image with modified prompt
        request_id = generate_image(image_prompt)
        if not request_id:
            raise HTTPException(status_code=500, detail="Failed to start image generation")
            
        # Poll for results
        max_attempts = 30
        for _ in range(max_attempts):
            result = retrieve_image_result(request_id)
            if result["status"] == "Ready":
                return {
                    "success": True,
                    "image_url": result["result"]["sample"]
                }
            await asyncio.sleep(1)
            
        raise HTTPException(status_code=408, detail="Image generation timed out")
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
