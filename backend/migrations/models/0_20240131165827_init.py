from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "text_messages" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "sim_number" VARCHAR(1000) NOT NULL,
    "detected_text" TEXT NOT NULL,
    "image_file" BYTEA,
    "blob_hash" VARCHAR(64) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
