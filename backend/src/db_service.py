from src.db_models import text_messages
from tortoise.exceptions import DoesNotExist, IntegrityError, OperationalError
from asyncpg.exceptions import DataError, UniqueViolationError


async def init_query(top: int):
    try:
        # Ensure 'top' is an integer and sanitize or validate it if necessary
        top = int(top)  # This also serves as basic validation

        # Using Tortoise ORM's query builder
        result = await text_messages.all().limit(top)
        
        data = [dict(message) for message in result]

        return data, None
    except ValueError:
        return None, "Invalid value for most recent values"
    except DoesNotExist:
        return None, "No values in table"
    except Exception as e:
        return None, str(e)
    

async def write_to_db(extracted_numbers, text, bin_contents, hex_digest):
    try:
        await text_messages.create(
            sim_number=extracted_numbers, 
            detected_text=text, 
            image_file=bin_contents, 
            blob_hash=hex_digest
        )

    except IntegrityError as e:
        return f"Integrity constraint violation: {e}"

    except DataError:
        return "Data does not fit schema"
    except OperationalError:
        return "Database operation failed"
    except Exception as e:
        return e
