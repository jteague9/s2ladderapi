# About
Python client for getting StarCraft II ladder data.

**Requires Python 3.6 or higher.**

Uses endpoints in https://develop.battle.net/documentation/api-reference/starcraft-2-community-api and https://develop.battle.net/documentation/api-reference/starcraft-2-game-data-api and other endpoints not noted in their centralized documentation.

Get your Blizzard client id and client secret from https://develop.battle.net/access/clients

# Example Usage
Prints out all the players in US Grandmaster
```Python
async def main(loop):
    blz = BlizzSession(os.environ['BLIZZARD_CLIENT_ID'], os.environ['BLIZZARD_CLIENT_SECRET'], loop=loop)
    await blz.get_token()
    season_id = (await blz.get_season('us'))['seasonId']
    result = await blz.get_ladders_by_region_league('us', season_id, 6)
    await blz.close()
    return result


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ladder_list = loop.run_until_complete(main(loop))
    for ladder in ladder_list:
        for team in ladder['team']:
            for player in team['member']:
                print(player)
```
