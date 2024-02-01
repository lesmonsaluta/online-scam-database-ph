from fastapi import FastAPI, File, UploadFile
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DBConnectionError
from tortoise import Tortoise

from src.ocr_script import process_image
from src.db_models import text_messages

import logging
import asyncio

import os
import hashlib
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = "5432"
db_name = os.getenv("POSTGRES_DB")

db_url = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

app = FastAPI()

TORTOISE_ORM = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": ["src.db_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Set to False because Aerich will handle migrations
    add_exception_handlers=True,
)

# register_tortoise(
#     app,
#     db_url=db_url,
#     modules={"models": ["src.db_models"]},
#     generate_schemas=True,
#     add_exception_handlers=True,
# )

# Define an endpoint to execute a custom SQL query
@app.get("/get-query/")
async def execute_custom_query():
    sql_query = "SELECT * FROM text_messages LIMIT 50;"
    try:
        result = await text_messages.raw(sql_query)
        return result
    except Exception as e:
        return {"error": str(e)}


@app.post("/upload-images/")
async def create_upload_file(files: list[UploadFile] = File(...)):
    results = {}
    for file in files:
        try:
            logging.info(f"Received {file.filename} for OCR processing")
            
            extracted_numbers, text = await asyncio.to_thread(process_image, file)

            contents = await file.read()
            bin_contents = contents

            hash_object = hashlib.sha256(bin_contents)
            hex_digest = hash_object.hexdigest()
            logging.info(f"Number and text extracted")
            
            # Write to DB
            await text_messages.create(sim_number=extracted_numbers, detected_text=text, image_file=bin_contents, blob_hash=hex_digest)
            logging.info(f"Details written to database")
            
            results[f'{file.filename}'] = { 'data' : 
                                        {
                                            'numbers' : extracted_numbers,
                                            'text' : text
                                        }}
                            

        except Exception as e:
            logging.error(f"Error processing file: {e}")
            
            results[f'{file.filename}'] = { 'data' : 
                                        {
                                            'error' : str(e)
                                        }}
                            
    return results

