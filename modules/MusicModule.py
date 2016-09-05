from discord.ext import commands
import discord
import asyncio


if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so')


class MusicModule:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx):

        channel = ctx.message.author.voice_channel
        try:
            voice = await self.bot.join_voice_channel(channel)
            player = await voice.create_ytdl_player('https://www.youtube.com/watch?v=MGk-TdNpD5w')
            player.start()
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(MusicModule(bot))
