
from discord.ext import commands
import resource
import discord


class InfoModule:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def heap(self):
        await self.bot.say('**Heap Size**')
        await self.bot.say('-------------')
        await self.bot.say(str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + ' kb')

    @commands.command()
    async def stats(self):
        await self.bot.say('**Signal Stats**')
        await self.bot.say('-------------------------')
        await self.bot.say('**Username**: ' + self.bot.user.name)
        await self.bot.say('**ID**: ' + self.bot.user.id)
        await self.bot.say('**Discord Version**: ' + discord.__version__)
        await self.bot.say('**Author**: Eleria')

    @commands.command()
    async def invite(self):
        await self.bot.say(str(discord.utils.oauth_url(client_id=self.bot.user.id)))
        await self.bot.say('This will only work with new Bot Applications. Sorry ')


def setup(bot):
    bot.add_cog(InfoModule(bot))
