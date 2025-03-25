from fastapi import FastAPI, APIRouter, Request, HTTPException
from api.routes import router as api_router  # if you modularize routes
import requests
import asyncio
from api.generateproblems import generate_image, retrieve_image_result

app = FastAPI()

router = APIRouter()

# Remove or comment this out since it's now in generateproblems.py
# @router.post("/process-exercise")
# async def process_exercise(request: Request):
#     ...

@router.post("/generate-image")
async def generate_image_endpoint(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt")
        
        # Start image generation
        request_id = generate_image(prompt)
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

app.include_router(api_router)  # Optional if you modularize
