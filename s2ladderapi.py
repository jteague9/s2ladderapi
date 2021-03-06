import aiohttp
from aiohttp import BasicAuth
import asyncio


class BlizzSession:

    # blizzard's api switches between str and int to represent regions but we will always expect str
    _regiond = {'us': 1, 'eu': 2, 'kr': 3}
    
    def __init__(self, client_id, client_secret, loop):
        self.client_id = client_id
        self.client_secret = client_secret
        self.loop = loop
        self._session = aiohttp.ClientSession(loop=self.loop)
        self.access_token = None

    async def close(self):
        await self._session.close()

    async def request(self, method, url, **kwargs):
        params = {'access_token': self.access_token}
        return await self._request(method, url, params=params, **kwargs)

    async def _request(self, method, url, **kwargs):
        async with self._session.request(method, url, **kwargs) as resp:
            try:
                return await resp.json()
            except Exception as e:
                return {}

    async def get_token(self):
        data = {'grant_type': 'client_credentials'}
        auth = BasicAuth(self.client_id, self.client_secret)
        url = 'https://us.battle.net/oauth/token'
        resp = await self._request('POST', url, data=data, auth=auth)
        self.access_token = resp['access_token']
        return resp

    """
    Profile API: Endpoints specific to profile information.
    """
    async def get_static_profile(self, region):
        """
        Returns all static SC2 profile data (achievements, categories, criteria, and rewards).
        :param region: The region of the data to retrieve.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/static/profile/{self._regiond[region]}'
        return await self.request('GET', url)

    async def get_metadata_profile(self, region, realm_id, profile_id):
        """
        Returns metadata for an individual's profile.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/metadata/profile/{self._regiond[region]}/{realm_id}/{profile_id}'
        return await self.request('GET', url)

    async def get_profile(self, region, realm_id, profile_id):
        """
        Returns data about an individual SC2 profile.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/profile/{self._regiond[region]}/{realm_id}/{profile_id}'
        return await self.request('GET', url)

    async def get_ladder_summary(self, region, realm_id, profile_id):
        """
        Returns a ladder summary for an individual SC2 profile.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/profile/{self._regiond[region]}/{realm_id}/{profile_id}/ladder/summary'
        return await self.request('GET', url)

    async def get_ladder_profile(self, region, realm_id, profile_id, ladder_id):
        """
        Returns data about an individual profile's ladder.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :param ladder_id: The ID of the ladder for which to retrieve data.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/profile/{self._regiond[region]}/{realm_id}/{profile_id}/ladder/{ladder_id}'
        return await self.request('GET', url)

    """
    Ladder API: Endpoints for general ladder information.
    """
    async def get_grandmaster_leaderboard(self, region):
        """
        Returns ladder data for the current season's grandmaster leaderboard.
        :param region: The region of the data to retrieve.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/ladder/grandmaster/{self._regiond[region]}'
        return await self.request('GET', url)

    async def get_season(self, region: int):
        """
        Returns data about the current season.
        :param region: The region of the data to retrieve.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/ladder/season/{self._regiond[region]}'
        return await self.request('GET', url)

    """
    Game Data API: Endpoints for StarCraft II ladder data.
    """
    async def get_ladder(self, region, ladder_id):
        """
        Returns data about a ladder division.
        :param region: The region of the data to retrieve.
        :param ladder_id: The ID of the ladder for which to retrieve data.
        :return:
        """
        url = f'https://{region}.api.blizzard.com/data/sc2/ladder/{ladder_id}'
        return await self.request('GET', url)

    async def get_league_data(self, region, season_id, queue_id, team_type, league_id):
        """
        Returns data for the specified season, queue, team, and league.
        :param region: The region of the data to retrieve.
        :param season_id:
        :param queue_id:
        :param team_type:
        :param league_id:
        :return:
        """
        url = f'https://{region}.api.blizzard.com/data/sc2/league/{season_id}/{queue_id}/{team_type}/{league_id}'
        return await self.request('GET', url)

    """
    Legacy API: Legacy endpoints that are still supported.
    """
    async def get_legacy_profile(self, region, realm_id, profile_id):
        """
        Retrieves data about an individual SC2 profile.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/profile/{self._regiond[region]}/{realm_id}/{profile_id}'
        return await self.request('GET', url)

    async def get_legacy_ladders(self, region, realm_id, profile_id):
        """
        Retrieves data about an individual SC2 profile's ladders.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/profile/{self._regiond[region]}/{realm_id}/{profile_id}/ladders'
        return await self.request('GET', url)

    async def get_legacy_match_history(self, region, realm_id, profile_id):
        """
        Returns data about an individual SC2 profile's match history.
        :param region: The region of the data to retrieve.
        :param realm_id: The region of the profile (1 or 2).
        :param profile_id: The profile ID.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/profile/{self._regiond[region]}/{realm_id}/{profile_id}/matches'
        return await self.request('GET', url)

    async def get_legacy_ladder(self, region, ladder_id):
        """
        Returns data about an individual SC2 ladder.
        :param region: The region of the data to retrieve.
        :param ladder_id: The ID of the ladder for which to retrieve data.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/ladder/{self._regiond[region]}/{ladder_id}'
        return await self.request('GET', url)

    async def get_legacy_achievements(self, region):
        """
        Returns data about the achievements available in SC2.
        :param region: The region of the data to retrieve.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/data/achievements/{self._regiond[region]}'
        return await self.request('GET', url)

    async def get_legacy_rewards(self, region):
        """
        Returns data about the rewards available in SC2.
        :param region: The region of the data to retrieve.
        :return:
        """
        url = f'https://us.api.blizzard.com/sc2/legacy/data/rewards/{self._regiond[region]}'
        return await self.request('GET', url)

    """
    Helper functions: Useful shortcut combinations of existing functions.
    """
    async def get_all_ladders(self):
        """
        Returns ladder data for all ranked 1v1 LotV ladders.
        :return: list
        """
        regions = ['us', 'eu', 'kr']
        result = await asyncio.gather(*[self.get_ladders_by_region(region) for region in regions])
        return [{'region': regions[0], 'data': result[0]},
                {'region': regions[1], 'data': result[1]},
                {'region': regions[2], 'data': result[2]}]

    async def get_ladders_by_region(self, region):
        """
        Returns ladder data for all ranked 1v1 LotV ladders in a region.
        :param region: The region of the data to retrieve.
        :return: list
        """
        season = await self.get_season(region)
        season_id = season['seasonId']
        result = await asyncio.gather(*[self.get_ladders_by_region_league(region, season_id, league)
                                      for league in range(7)])
        return [ladder for league in result for ladder in league]

    async def get_ladders_by_region_league(self, region, season_id, league, game_type=201, team_type=0):
        """
        Returns ladder data for all ranked 1v1 LotV ladders in a region and league.
        :param region: The region of the data to retrieve.
        :param season_id:
        :param league:
        :param game_type:
        :param team_type:
        :return: list
        """
        league_data = await self.get_league_data(region, season_id, game_type, team_type, league)
        ladder_ids = []
        for tier in league_data.get('tier', []):
            for div in tier['division']:
                ladder_ids.append(div['ladder_id'])
        return await asyncio.gather(*[self.get_ladder(region, ladder_id) for ladder_id in ladder_ids])
