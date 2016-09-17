from discord.ext import commands
import discord
import requests
from config import riot_api as key
import modules.utils.league
import os

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
        cwd = os.getcwd()
        obs_url = 'https://na.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/NA1/'+ summoner_id +'?api_key=' + key
        obs = requests.get(obs_url).json()
        try:
            enc_key = obs['observers']['encryptionKey']
            mathchid = obs['gameId']
        except:
            code = obs['status']['status_code']
            if code == 404:
                await self.bot.say('Summoner is not ingame :thunder_cloud_rain:')
            else:
                await self.bot.say('Unknown Error has occured :anger:')

        cmd = """ ```cd "C:\\Riot Games\\League of Legends\\RADS\\solutions\\lol_game_client_sln\\releases\\0.0.1.145\\deploy" \n
        start "" "League of Legends.exe" "8394" "LoLLauncher.exe" "" "spectator spectator.na.lol.riotgames.com:80 {0} {1} NA1" "-UseRads" ```""".format(enc_key, mathchid)
        await self.bot.say("Please paste the following into your cmd or use the .bat provided")
        await self.bot.say(cmd)
        cmdfile = cmd.replace("`", "")
        file = open(cwd + '\\cache\\{0}_spectate.bat'.format(mathchid), 'w')
        file.write(cmdfile)
        file.close()
        f1 = open(cwd + '\\cache\\{0}_spectate.bat'.format(mathchid), 'r')

        await self.bot.send_file(ctx.message.channel, f1)
        f1.close()

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
            else:
                await self.bot.say('League Status for {0} \n'
                                '-----------------------\n'
                                'Host: {1} \n'
                                'Game Status: {2}\n'
                                'Shop Status: {3}\n'
                                'Website Status: {4}\n'
                                'Client Status {5}\n'
                                'Alpha Status: {6}'.format(name, hostname, Game_status, Shop_status, website_status, client_status,alpha))

    @commands.command(pass_context=True, help='Shows the FTP Champions | Under Construction')
    async def free2play(self, ctx):
        try:
            url = 'https://euw.api.pvp.net/api/lol/euw/v1.2/champion?freeToPlay=true&api_key=' + key
            f2p = requests.get(url).json()
            a = []
            for i in range(10):
                a.append(int(f2p['champions'][i]['id']))
            url2 = 'https://global.api.pvp.net/api/lol/static-data/euw/v1.2/champion?champData=info&api_key=' + key
            champs = requests.get(url2).json()
            await self.bot.say('**Free to Play Champions**\n'
                           '---------------------------')
            for value in champs["data"].items():
                if int(value['id'] in a):
                    await self.bot.say(value['name'] + " - " + value['title'])
        except:
            await self.bot.say('This Command is under construction')


def setup(bot):
    bot.add_cog(LeagueModule(bot))
