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

    @commands.command(pass_context=True, help='Joins a server')
    @modules.utils.utils.is_owner()
    async def add(self, ctx, *, invite:str):
        try:
            await self.bot.say(str(invite))
            await self.bot.accept_invite(str(invite))
            await self.bot.say('Done')
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(AdministrationModule(bot))
