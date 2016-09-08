from discord.ext import commands
import discord

if discord.opus.is_loaded() is False:  # Läd Opus Lib
    discord.opus.load_opus('opus')


class MusicModule:

    def __init__(self, bot):
        self.bot = bot
        self.player = None
        self.voice = None

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        channel = ctx.message.author.voice_channel
        if channel is None:
            await self.bot.say('You have to be in a voice channel in Order to use this.')
            return False
        else:

            if self.voice is None:
               self.voice = voice = await self.bot.join_voice_channel(channel)
            else:
                await self.voice.move_to(channel)
            return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song: str):
        voice = self.voice
        opts = {'default_search': 'auto'}
        if voice is None:
            await ctx.invoke(self.summon)
        try:
           self.player = player = await voice.create_ytdl_player(song, ytdl_options=opts)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            await self.bot.say('Playing {0}'.format(player.title))
            player.start()

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        player = self.player
        if player.is_playing():
            player.volume = value / 100
            await self.bot.say('Set the volume to {:.0%}'.format(player.volume))
        else:
            await self.bot.say('There is nothing playing')

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        player = self.player
        if player.is_playing():
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        player = self.player
        if not player.is_playing():
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        server = ctx.message.server
        player = self.player
        voice = self.voice

        if player.is_playing():
            player.stop()

        try:
            voice.audio_player.cancel()
            await voice.disconnect()
        except:
            pass


def setup(bot):
    bot.add_cog(MusicModule(bot))
