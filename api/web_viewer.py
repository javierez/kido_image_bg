from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from supabase_connector import get_stories
import os

app = FastAPI()

# Get the absolute path to the templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    stories = get_stories()
    return templates.TemplateResponse("stories.html", {"request": request, "stories": stories})