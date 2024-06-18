from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.photo_handler.handlers import get_photo, list_photos, save_photo
from .send_email.schemas import FormData
from .send_email.email_utils import send_email

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
        # logger.info(f"Received form data: {form_data.json()}")
        response = send_email(form_data)
        return response
    except Exception as e:
        logger.error(f"Error handling form submission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/photos/{photo_name}")
async def handle_get_photo(photo_name: str):
    return get_photo(photo_name)


@app.get("/photos")
async def handle_list_photos():
    photos = list_photos()
    base_url = "http://localhost:8000/photos"
    photo_urls = [f"{base_url}/{photo}" for photo in photos["photos"]]
    return {"photos": photo_urls}


@app.post("/photos/")
async def handle_upload_photo(file: UploadFile = File(...)):
    try:
        return save_photo(file.file.read(), file.filename)
    except Exception as e:
        logger.error(f"Error saving photo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
