from discord.ext import commands
from collections import Counter
import discord


class InfoModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='TEST')
    async def info(self):
        message = ['**Signal Stats**']
        message.append('-Name: ' + self.bot.user.name)
        message.append('-ID: ' + self.bot.user.id)
        message.append('- Servers: {}'.format(len(self.bot.servers)))
        channel_types = Counter(c.type for c in self.bot.get_all_channels())
        voice = channel_types[discord.ChannelType.voice]
        text = channel_types[discord.ChannelType.text]
        message.append('- {} text channels, {} voice channels'.format(text, voice))
        message.append('')
        message.append('-Signal Server: ')
        await self.bot.say('\n'.join(message))

    @commands.command()
    async def invite(self):
        await self.bot.say(str(discord.utils.oauth_url(client_id=self.bot.user.id)))
        await self.bot.say('This will only work with new Bot Applications. Sorry ')


def setup(bot):
    bot.add_cog(InfoModule(bot))
