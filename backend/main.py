from fastapi import File, UploadFile
from src.app_factory import create_app

from src.ocr_service import process_image
from src.db_models import text_messages
from src.db_service import init_query

from src.logger_setup import logger_service

import asyncio
import hashlib

"""
Uses src/app_factory.py for instantiation of the app, as well as connection to the DB via register_tortoise. 
"""
app = create_app()
logger = logger_service.logger_init()

# # Define an endpoint to execute a custom SQL query
# @app.get("/home-query/")
# async def home_query():
#     data, error = init_query(50)
    
#     if error:
        
#     return
#! Need to define schema between frontend and backend, need to decorate this
#! For internal communication between services, (data, error) is okay
#! Need to plan out for frontend

@app.post("/upload-images/")
async def create_upload_file(files: list[UploadFile] = File(...)):
    results = {}
    for file in files:
        try:
            logger.info(f"Received {file.filename} for OCR processing")

            extracted_numbers, text = await asyncio.to_thread(process_image, file)

            contents = await file.read()
            bin_contents = contents

            hash_object = hashlib.sha256(bin_contents)
            hex_digest = hash_object.hexdigest()
            logger.info(f"Number and text extracted")

            # Write to DB
            await text_messages.create(sim_number=extracted_numbers, detected_text=text, image_file=bin_contents, blob_hash=hex_digest)
            # schema, from text_messages_service import write_to_db
            # write_to_db ganito ganyan
            logger.info(f"Details written to database")

            results[f'{file.filename}'] = { 'data' :
                                        {
                                            'numbers' : extracted_numbers,
                                            'text' : text
                                        }}


        except Exception as e:
            logger.error(f"Error processing file: {e}")

            results[f'{file.filename}'] = { 'data' :
                                        {
                                            'error' : str(e)
                                        }}

    return results

