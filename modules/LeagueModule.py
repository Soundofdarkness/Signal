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
        try:
            summoner_id = str(rsumonner[summonernamerequest]['id'])
            pfp_id = str(rsumonner[summonernamerequest]['profileIconId'])
            level = str(rsumonner[summonernamerequest]['summonerLevel'])
        except:
            exception = rsumonner['status']['status_code']
            info = rsumonner['status']['message']
            if exception == 404:
                await self.bot.say('Summoner not found')
                await self.bot.say('`{0}`'.format(info))
                return True
            elif exception == 429:
                await self.bot.say('Rate limit is exceeded :thunder_cloud_rain:')
                return True
            elif exception == 500:
                await self.bot.say('Unknown Error! Everybody panic !')
                return True
            elif exception == 503:
                await self.bot.say('Service Unavailable. Please check again later.')
                return True
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

    @commands.command(pass_context=True, help='Shows the status for the given platform')
    async def lolstatus(self, ctx, platform:str):
        url = 'http://status.leagueoflegends.com/shards/' + platform
        status_parse = requests.get(url).json()
        try:
            name = status_parse['name']
            Game_status = status_parse['services'][0]['status']
            Shop_status = status_parse['services'][1]['status']
            website_status = status_parse['services'][2]['status']
            client_status = status_parse['services'][3]['status']
            alpha = status_parse['services'][4]['status']
            hostname = status_parse['hostname']
        except:
            alpha = 'Shut down'
        await self.bot.say('League Status for {0} \n'
                          '-----------------------\n'
                          'Host: {1} \n'
                          'Game Status: {2}\n'
                          'Shop Status: {3}\n'
                          'Website Status: {4}\n'
                          'Client Status {5}\n'
                          'Alpha Status: {6}'.format(name, hostname, Game_status, Shop_status, website_status, client_status,alpha))

    @commands.command(pass_context=True, help='Shows the FTP Champions')
    async def freetoplay(self, ctx):
        url = 'https://euw.api.pvp.net/api/lol/euw/v1.2/champion?freeToPlay=true&api_key=' + key
        f2p = requests.get(url).json()
        try:
            c1 = f2p['champions'][0]['id']
            c2 = f2p['champions'][1]['id']
            c3 = f2p['champions'][2]['id']
            c4 = f2p['champions'][3]['id']
            c5 = f2p['champions'][4]['id']
            c6 = f2p['champions'][5]['id']
            c7 = f2p['champions'][6]['id']
            c8 = f2p['champions'][7]['id']
            c9 = f2p['champions'][8]['id']
            c10 = f2p['champions'][9]['id']
        except Exception as e:
            fmt = 'An error occurred while processing the Riot API data: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        champ_url1 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c1) + '?api_key=' + key
        champ_url2 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c2) + '?api_key=' + key
        champ_url3 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c3) + '?api_key=' + key
        champ_url4 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c4) + '?api_key=' + key
        champ_url5 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c5) + '?api_key=' + key
        champ_url6 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c6) + '?api_key=' + key
        champ_url7 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c7) + '?api_key=' + key
        champ_url8 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c8) + '?api_key=' + key
        champ_url9 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c9) + '?api_key=' + key
        champ_url10 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion/' + str(c10) + '?api_key=' + key
        champ_url1 = champ_url1.replace(",", "")
        champ_url2 = champ_url2.replace(",", "")
        champ_url3 = champ_url3.replace(",", "")
        champ_url4 = champ_url4.replace(",", "")
        champ_url5 = champ_url5.replace(",", "")
        champ_url6 = champ_url6.replace(",", "")
        champ_url7 = champ_url7.replace(",", "")
        champ_url8 = champ_url8.replace(",", "")
        champ_url9 = champ_url9.replace(",", "")
        champ_url10 = champ_url10.replace(",", "")

        cj1 = requests.get(champ_url1).json()
        cj2 = requests.get(champ_url2).json()
        cj3 = requests.get(champ_url3).json()
        cj4 = requests.get(champ_url4).json()
        cj5 = requests.get(champ_url5).json()
        cj6 = requests.get(champ_url6).json()
        cj7 = requests.get(champ_url7).json()
        cj8 = requests.get(champ_url8).json()
        cj9 = requests.get(champ_url9).json()
        cj10 = requests.get(champ_url10).json()
        ce1 = cj1['name']
        ce2 = cj2['name']
        ce3 = cj3['name']
        ce4 = cj4['name']
        ce5 = cj5['name']
        ce6 = cj6['name']
        ce7 = cj7['name']
        ce8 = cj8['name']
        ce9 = cj9['name']
        ce10 = cj10['name']
        await self.bot.say('Free to play Champions\n'
                            '-----------------------\n'
                            '- {0}\n'
                            '- {1}\n'
                            '- {2}\n'
                            '- {3}\n'
                            '- {4}\n'
                            '- {5}\n'
                            '- {6}\n'
                            '- {7}\n'
                            '- {8}\n'
                            '- {9}'.format(ce1, ce2, ce3, ce4, ce5, ce6, ce7, ce8, ce9, ce10))


def setup(bot):
    bot.add_cog(LeagueModule(bot))
