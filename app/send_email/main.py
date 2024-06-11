from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from .schemas import FormData
from .email_utils import send_email

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/submit")
async def handle_form_submission(form_data: FormData):
    try:
        logger.info(f"Received form data: {form_data.json()}")
        response = send_email(form_data)
        return response
    except Exception as e:
        logger.error(f"Error handling form submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
