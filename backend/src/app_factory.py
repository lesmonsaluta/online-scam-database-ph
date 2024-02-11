from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = "5432"
db_name = os.getenv("POSTGRES_DB")

db_url = f"postgres://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

def create_app():
    app = FastAPI()

    TORTOISE_ORM = {
        "connections": {
            "default": db_url
            },
        
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
    
    return app