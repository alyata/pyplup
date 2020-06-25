from showdown import Showdown
import asyncio
import time

async def main():
    show = Showdown('kapzlok2408', password = 'chandra2408')
    await show.connect()
    task = asyncio.create_task(show.run())

    #await show.close()
    await task

if __name__ == "__main__":
    asyncio.run(main())
