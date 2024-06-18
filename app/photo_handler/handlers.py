import os
from fastapi import HTTPException
from fastapi.responses import FileResponse
from PIL import Image
from io import BytesIO

# Обновляем путь к директории photos
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "..", "photos")


def get_photo(photo_name: str):
    file_path = os.path.join(PHOTOS_DIR, photo_name)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Photo not found")
    return FileResponse(file_path)


def list_photos():
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
    photos = os.listdir(PHOTOS_DIR)

    # Фильтруем системные файлы
    photos = [photo for photo in photos if not photo.startswith('.')]

    return {"photos": photos}


def save_photo(file: bytes, filename: str):
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)

    # Открываем изображение из переданных байтов
    image = Image.open(BytesIO(file))

    # Конвертируем изображение в RGB и сохраняем как JPEG
    rgb_image = image.convert('RGB')
    jpeg_filename = os.path.splitext(filename)[0] + ".jpg"
    file_path = os.path.join(PHOTOS_DIR, jpeg_filename)
    rgb_image.save(file_path, format='JPEG')

    return {"filename": jpeg_filename}
