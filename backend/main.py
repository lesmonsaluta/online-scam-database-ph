from fastapi import File, UploadFile
from src.app_factory import create_app

from src.ocr_service import process_image
from src.db_models import text_messages

import logging

import asyncio
import hashlib

"""
Uses src/app_factory.py for instantiation of the app, as well as connection to the DB via register_tortoise. 
"""
app = create_app()


# Define an endpoint to execute a custom SQL query
@app.get("/home-query/")
async def execute_custom_query():
    sql_query = "SELECT * FROM text_messages LIMIT 50;"
    try:
        result = await text_messages.raw(sql_query)
        return result
    except Exception as e:
        return {"error": str(e)}
    # add to another file, call the func or class there
    # text_msgs service


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
            # schema, from text_messages_service import write_to_db
            # write_to_db ganito ganyan
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

