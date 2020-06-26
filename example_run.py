from src.showdown import Showdown
import asyncio
import time

import example_config as config

async def main():
    show = Showdown(config.username, config.password)
    await show.connect()
    task = asyncio.create_task(show.run())

    #await show.close()
    await task

if __name__ == "__main__":
    asyncio.run(main())
