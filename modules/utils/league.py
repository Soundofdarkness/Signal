import requests
from config import riot_api as key


def summoner_to_id(platform: str, summoner: str):
    summonernamerequest = summoner.replace(" ", "")
    summonernamerequest = summonernamerequest.lower()
    url = 'https://' + platform + '.api.pvp.net/api/lol/' + platform + '/v1.4/summoner/by-name/' + summoner + '?api_key=' + key
    rsumonner = requests.get(url).json()
    summoner_id = str(rsumonner[summonernamerequest]['id'])
    return summoner_id

