import sys
import asyncio


async def set_timer(time):
    for remaining in range(time, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        await asyncio.sleep(1)
