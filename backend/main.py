from fastapi import File, UploadFile
from src.app_factory import create_app

from src.ocr_service import process_image
from src.db_service import init_query, write_to_db

from src.logger_setup import logger_service

from src.schemas import InternalErrorResponseSchema, ResponseDataSchema, ImageUploadResponseSchema, ExternalResponseSchema

import asyncio

"""
Uses src/app_factory.py for instantiation of the app, as well as connection to the DB via register_tortoise
Uses src/logger_setup/logger_service to instantiate a logger
"""
app = create_app()
logger = logger_service.logger_init()

# Endpoint triggered upon home screen launch, for scrolling design
@app.get("/home-query/", response_model=ExternalResponseSchema)
async def home_query():
    data, error = await init_query(50)
    
    if error:
        logger.error(f"Failed to extract data for home page: {error}")
        response_object = ExternalResponseSchema(results=None,
                                                 error=error,
                                                 success=False)
        
        return response_object
    else:
        logger.info("Successfully extracted for home page")
        response_object = ExternalResponseSchema(results=data,
                                                 error=None,
                                                 success=True)
        
        return response_object


# Endpoint triggered upon image uploads
@app.post("/upload-images/", response_model=ExternalResponseSchema)
async def create_upload_file(files: list[UploadFile] = File(...)):
    logger.info("Received payload")
    results = {}
    
    for file in files:
        logger.info(f"Processing {file.filename}")
        
        # OCR Extraction, BIN extraction, hashing of BIN for entry unique id
        (extracted_numbers, text, bin_contents, hex_digest), file_error = await asyncio.to_thread(process_image, file)
        if file_error:
            logger.error(f"Error for {file.filename}: {file_error}")
            results[file.filename] = ImageUploadResponseSchema(data=None, error=file_error, success=False)
            continue
        logger.info(f"Number and text extracted for {file.filename}")

        # write to POSTGRES DB
        db_error = await write_to_db(extracted_numbers, text, bin_contents, hex_digest)
        if db_error:
            logger.error(f"Error for {file.filename}: {db_error}")
            results[file.filename] = ImageUploadResponseSchema(data=None, error=str(db_error), success=False)
            continue
        logger.info(f"Written onto DB for {file.filename}")

        # No errors encountered, add to response dict
        results[file.filename] = ImageUploadResponseSchema(
            data=ResponseDataSchema(
                numbers=extracted_numbers, 
                text=text
                ), 
            error=None, 
            success=True)
        
    response_object = {'results': results,
                       'error': None,
                       'success': True}
    
    logger.info("Finished processing payload")
    return response_object

## API

## MODEL

## COOKIES AND SESSION ID