from discord.ext import commands
import random
import modules.utils.warframe
import datetime
from modules.utils.warframejokes import jokes
import modules.utils.utils


class WarframeModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='voidtrader', help='Shows the current Void Traders')
    async def void_traders(self):
        ws = modules.utils.warframe.get_worldstate()
        trader_loc = ws['VoidTraders'][0]['Node']
        trader_relay = modules.utils.warframe.id_to_relay(trader_loc)
        trader_name = "Baro Ki'Teer"
        activation = ws['VoidTraders'][0]['Activation']['sec']
        expire = ws['VoidTraders'][0]['Expiry']['sec']
        activation_date = datetime.datetime.fromtimestamp(activation).strftime('%Y-%m-%d %H:%M:%S')
        expire_date = datetime.datetime.fromtimestamp(expire).strftime('%Y-%m-%d %H:%M:%S')
        await self.bot.say('**Current Void Trader**\n'
                           '-------------------------\n'
                           'Name: {0}\n'
                           'Location/Node: {1}\n'
                           'Activation at: {2}\n'
                           'Expiry at: {3}'.format(trader_name, trader_relay, activation_date, expire_date))

    @commands.command(help='Shows the Daily Deals')
    async def deals(self):
        ws = modules.utils.warframe.get_worldstate()
        raw_item = ws['DailyDeals'][0]['StoreItem']
        act = ws['DailyDeals'][0]['Activation']['sec']
        a_date = datetime.datetime.fromtimestamp(act).strftime('%Y-%m-%d %H:%M:%S')
        exp = ws['DailyDeals'][0]['Expiry']['sec']
        e_date = datetime.datetime.fromtimestamp(exp).strftime('%Y-%m-%d %H:%M:%S')
        discount = ws['DailyDeals'][0]['Discount']
        price = ws['DailyDeals'][0]['SalePrice']
        anmount = ws['DailyDeals'][0]['AmountTotal']
        sold = ws['DailyDeals'][0]['AmountSold']
        item_name = modules.utils.warframe.item_to_name(raw_item)
        await self.bot.say('**Daily Deals**\n'
                           '-------------------\n'
                           'Item: {0}\n'
                           'Activation at: {1}\n'
                           'Expiry at: {2}\n'
                           'Price: {3}\n'
                           'Discount: {4}\n'
                           'Total Amount: {5}\n'
                           'Already sold: {6}'.format(item_name, a_date, e_date, price, discount, anmount, sold))

    @commands.command(help='Shows the Invasions')
    async def invasions(self):
        ws = modules.utils.warframe.get_worldstate()
        invasions = ws['Invasions']
        count = len(invasions)
        await self.bot.say('**Invasions**')
        await self.bot.say('-------------')
        l = range(count)
        for each in l:
            is_done = invasions[each]['Completed']

            f_raw = invasions[each]['Faction']
            faction = modules.utils.warframe.faction_to_name(f_raw)
            node_raw = invasions[each]['Node']
            node = modules.utils.warframe.node_to_name(node_raw)
            goal = str(invasions[each]['Goal'])
            loc_tag = invasions[each]['LocTag']
            loc = modules.utils.warframe.string_to_name(loc_tag)
            act = invasions[each]['Activation']['sec']
            act_d = datetime.datetime.fromtimestamp(act).strftime('%Y-%m-%d %H:%M:%S')
            await self.bot.say('*Completed*: {5}\n'
                               '*Faction*: {0}\n'
                               '*Node*: {1}\n'
                               '*Goal*: {2}\n'
                               '*Activation at*:{3}\n'
                               '*Info*: {4}'.format(faction, node, goal, act_d, loc, str(is_done)))
            await self.bot.say('-------------------------')

    @commands.command(help='Shows Warframe Alerts')
    async def alerts(self):
        ws = modules.utils.warframe.get_worldstate()
        alerts = ws['Alerts']
        count = len(alerts)
        await self.bot.say('**Alerts**')
        await self.bot.say('--------------')
        l = range(count)
        for number in l:
            al = alerts[number]
            act_raw = al['Activation']['sec']
            act = datetime.datetime.fromtimestamp(act_raw).strftime('%Y-%m-%d %H:%M:%S')
            exp_raw = al['Expiry']['sec']
            exp = datetime.datetime.fromtimestamp(exp_raw).strftime('%Y-%m-%d %H:%M:%S')
            missiondata = al['MissionInfo']
            type_raw = missiondata['missionType']
            ty = modules.utils.warframe.mission_to_name(type_raw)
            fac_raw = missiondata['faction']
            fac = modules.utils.warframe.faction_to_name(fac_raw)
            loc_raw = missiondata['location']
            loc = modules.utils.warframe.node_to_name(loc_raw)
            min_en = missiondata['minEnemyLevel']
            max_en = missiondata['maxEnemyLevel']
            dif_raw = missiondata['difficulty']
            dif = modules.utils.warframe.difficulty_parse(str(dif_raw))
            creds = str(missiondata['missionReward']['credits'])
            await self.bot.say('*Type*: {0}\n'
                               '*Faction*: {1}\n'
                               '*Location*: {2}\n'
                               '*Min Enemy LvL*: {3}\n'
                               '*Max Enemy Lvl*: {4}\n'
                               '*Difficulty*: {5}\n'
                               '*Award*: {6} cr\n'
                               '*Activation*: {7}\n'
                               '*Expiry*: {8}\n'
                               '---------------------'.format(ty, fac, loc, min_en, max_en, dif, creds, act, exp))

    @commands.command(help='Shows a Warframe Joke')
    async def joke(self):
        lenght = len(jokes)
        number = random.randrange(0, lenght, step=1)
        joke = jokes[number]
        await self.bot.say(joke)


def setup(bot):
    bot.add_cog(WarframeModule(bot))
