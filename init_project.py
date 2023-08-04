from main.models import database
import asyncio


if __name__ == "__main__":
    asyncio.run(database.start())
