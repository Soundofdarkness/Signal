from discord.ext import commands
import discord
import requests
from config import riot_api as key
import modules.utils.league

class LeagueModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, help="Displays League stats for a given Summoner.")
    async def league(self, ctx, platform: str, *, summoner: str):
        if platform == 'eune':
            platformcm = 'eun'
        else:
            platformcm = platform
        summonernamerequest = summoner.replace(" ", "")
        summonernamerequest = summonernamerequest.lower()
        url = 'https://' + platform + '.api.pvp.net/api/lol/' + platform + '/v1.4/summoner/by-name/' + summoner + '?api_key=' + key
        rsumonner = requests.get(url).json()
        summoner_id = str(rsumonner[summonernamerequest]['id'])
        pfp_id = str(rsumonner[summonernamerequest]['profileIconId'])
        level = str(rsumonner[summonernamerequest]['summonerLevel'])
        tier_url = 'https://' + platform + '.api.pvp.net/api/lol/' + platform + '/v2.5/league/by-summoner/' + summoner_id + '/entry?api_key=' + key
        try:
            league = requests.get(tier_url).json()
            league_name = league[summoner_id][0]['name']
            league_tier = league[summoner_id][0]['tier']
            league_division = league[summoner_id][0]['entries'][0]['division']
        except:
            league_name = 'No League'
            league_tier = 'No Rank'
            league_division = 'No Division'
        try:
            cmastery_url = 'https://' + platform + '.api.pvp.net/championmastery/location/' + platformcm + '1/player/' + summoner_id + '/topchampions?count=1&api_key=' + key
            cmastery = requests.get(cmastery_url).json()
            champ_id = cmastery[0]['championId']
            points = cmastery[0]['championPoints']
            champ_url = 'https://global.api.pvp.net/api/lol/static-data/' + platform + "/v1.2/champion/" + str(champ_id) + '?api_key=' + key
            champ_json = requests.get(champ_url).json()
            champname = champ_json['name']
        except:
            champname = 'No Champion'

        av_url = 'http://ddragon.leagueoflegends.com/cdn/6.18.1/img/profileicon/'+ pfp_id + '.png'
        await self.bot.say('**{0}**\n'
                           '---------------\n'
                           '*Level*: {1}\n'
                           '*League Name*: {2}\n'
                           '*League Tier*: {3}\n'
                           '*Division*: {5}\n'
                           '*Avatar URL*: {4}'.format(summoner, level, league_name, league_tier, av_url, league_division))
        await self.bot.say('**Championmastery**\n'
                           '--------------------\n'
                           '*Champion*: {0}\n'
                           'Mastery Points: {1}'.format(champname, points))

    @commands.command(pass_context=True, help='Spectates a given User.Atm NA only')
    async def spectate(self, ctx, *, summoner: str):
        summoner_id = modules.utils.league.summoner_to_id('na', summoner)
        obs_url = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/'+ summoner_id +'?api_key=' + key
        obs = requests.get(obs_url).json()
        enc_key = obs['observers']['encryptionKey']
        mathchid = obs['gameId']

        cmd = """ ```cd "C:\\Riot Games\\League of Legends\\RADS\\solutions\\lol_game_client_sln\\releases\\0.0.1.145\\deploy" \n
        start "" "League of Legends.exe" "8394" "LoLLauncher.exe" "" "spectator spectator.na.lol.riotgames.com:80 {0} {1} NA1" "-UseRads" ```""".format(enc_key, mathchid)
        await self.bot.say("Please paste the following into your cmd")
        await self.bot.say(cmd)

def setup(bot):
    bot.add_cog(LeagueModule(bot))
