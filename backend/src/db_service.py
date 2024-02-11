from src.db_models import text_messages
from tortoise.exceptions import DoesNotExist

async def init_query(top: int):
    try:
        # Ensure 'top' is an integer and sanitize or validate it if necessary
        top = int(top)  # This also serves as basic validation

        # Using Tortoise ORM's query builder
        result = await text_messages.all().limit(top)
        
        # Convert the result to a list of dicts (or another preferred format)
        data = [dict(message) for message in result]

        return data, None
    except ValueError:
        return None, "Invalid value for most recent values"
    except DoesNotExist:
        return None, "No values in table"
    except Exception as e:
        return None, str(e)
