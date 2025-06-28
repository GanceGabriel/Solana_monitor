from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from app.routes.validator import router as validator_router
from dotenv import load_dotenv

import os

load_dotenv()  # Încarcă variabilele din .env

app = FastAPI()

# Montăm folderul static pentru CSS, JS, imagini etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Middleware CORS (permite cereri cross-origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # poți limita domeniile aici dacă vrei
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Înregistrăm router-ul din validator.py
app.include_router(validator_router)

# Setăm directorul cu template-uri
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Renderizăm pagina index.html cu contextul request
    return templates.TemplateResponse("index.html", {"request": request})

