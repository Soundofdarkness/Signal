from discord.ext import commands
import discord
import modules.utils.utils


class AdministrationModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, help='Sets the bots playing status')
    @modules.utils.utils.is_owner()
    async def setgame(self, ctx, *game):
        gameName = ' '.join(game)
        await self.bot.change_status(game=discord.Game(name=gameName))
        await self.bot.say('Game changed to **{0}** :smile:'.format(gameName))


def setup(bot):
    bot.add_cog(AdministrationModule(bot))
