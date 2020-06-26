from src.showdown import Showdown
import asyncio
import time

import example_config as config

async def main():
    #setup the API
    show = Showdown(config.username, config.password)
    #open a connection to the server
    await show.connect()
    #start the processing loop
    task = asyncio.create_task(show.run())
    #wait for bot to terminate itself,
    #which should only happen if a fatal error is encountered
    await task

if __name__ == "__main__":
    asyncio.run(main())
