import asyncio
import os
from s2ladderapi import BlizzSession


async def main(loop):
    blz = BlizzSession(os.environ['BLIZZARD_CLIENT_ID'], os.environ['BLIZZARD_CLIENT_SECRET'], loop=loop)
    await blz.get_token()
    data = await blz.get_grandmaster_leaderboard('us')
    await blz.close()
    return data


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(main(loop))
    print(data)


