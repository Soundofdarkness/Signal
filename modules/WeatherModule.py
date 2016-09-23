import pyowm
from discord.ext import commands
import discord
from config import OWMKey as key


class WeatherModule:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, help='Shows the current weather')
    async def weather(self, ctx, city:str , code: str):
        owm = pyowm.OWM(key)
        observation = owm.weather_at_place(city + ',' + code)
        w = observation.get_weather()
        temp = w.get_temperature(unit='celsius')
        press = w.get_pressure()
        status = w.get_detailed_status()#
        sunset = w.get_sunset_time('iso')
        await self.bot.say('Weather for : **{0}** \n'
                           '------------------------\n'
                           'Status: {1}\n'
                           'Current Temp : {3} °C \n'
                           'Max: {4} Min: {5}\n'
                           'Pressure: {6} hPa\n'
                           ':city_sunset: {2}'.format(city, status, sunset, temp['temp'],temp['temp_max'], temp['temp_min'],press['press']))


def setup(bot):
    bot.add_cog(WeatherModule(bot))
