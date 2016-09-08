from discord.ext import commands
from collections import Counter
import discord



class InfoModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Shows basic stats for the Bot')
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

    @commands.command(help='Shows the invite OAuth Link for the Bot')
    async def invite(self):
        await self.bot.say(str(discord.utils.oauth_url(client_id=self.bot.user.id)))
        await self.bot.say('This will only work with new Bot Applications. Sorry ')

    @commands.command(pass_context=True, help='Shows the avatar for a given Member.')
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        await self.bot.say(('{0.name} has this avatar: {0.avatar_url}'.format(member)))

    @commands.command(pass_context=True, help='Shows Info about the server', no_pm=True)
    async def serverinfo(self, ctx):
        server = ctx.message.server
        await self.bot.say('**{0.name}**\n'
                           '----------------------\n'
                           '-ID: {0.id}\n'
                           '-Created at: {0.created_at}\n'
                           '-Owner: {0.owner}\n'
                           '-Icon: {0.icon_url}'.format(server))

    @commands.command(pass_context=True, help='Shows info about a channel')
    async def channelinfo(self, ctx, channel: discord.Channel = None):
        if channel is None:
            channel = ctx.message.channel

        if channel.is_private:
            await self.bot.say('**Private Channel**\n'
                               '---------------------\n'
                               '-ID: {0.id}\n'
                               '-Created at: {0.created_at}'.format(channel))
        else:
            await self.bot.say('**{0.name}**\n'
                               '---------------------\n'
                               '-ID: {0.id}\n'
                               '-Topic: {0.topic}\n'
                               '-Position: {0.position}\n'
                               '-Created at: {0.created_at}'.format(channel))


def setup(bot):
    bot.add_cog(InfoModule(bot))
