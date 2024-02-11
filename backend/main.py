from fastapi import File, UploadFile
from src.app_factory import create_app

from src.ocr_service import process_image
from src.db_service import init_query, write_to_db

from src.logger_setup import logger_service

import asyncio

"""
Uses src/app_factory.py for instantiation of the app, as well as connection to the DB via register_tortoise
Uses src/logger_setup/logger_service to instantiate a logger
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

# Endpoint triggered upon image uploads
@app.post("/upload-images/")
async def create_upload_file(files: list[UploadFile] = File(...)):
    results = {}
    
    for file in files:
        logger.info(f"Received {file.filename} for OCR processing")
        
        # Process the image
        (extracted_numbers, text, bin_contents, hex_digest), file_error = await asyncio.to_thread(process_image, file)
        if file_error:
            logger.error(f"{file_error} for {file.filename}")
            results[f'{file.filename}'] = {'data' : None,
                                           'error' : file_error}
            continue
        logger.info(f"Number and text extracted for {file.filename}")

        # Write to DB Service
        db_error = await write_to_db(extracted_numbers, text, bin_contents, hex_digest)
        if db_error:
            logger.error(f"Error for {file.filename}: {db_error}")
            results[f'{file.filename}'] = {'data' : None,
                                           'error' : str(db_error)}
            continue
    

        results[f'{file.filename}'] = {'data' : {'numbers' : extracted_numbers,
                                                    'text' : text},
                                        'error' : None}

    return results
    #! Need to define schema between frontend and backend, need to decorate this
    #! For internal communication between services, (data, error) is okay
    #! Need to plan out for frontend