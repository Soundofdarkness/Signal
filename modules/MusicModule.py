from discord.ext import commands
import discord


if not discord.opus.is_loaded():
    discord.opus.load_opus('/usr/lib/x86_64-linux-gnu/libopus.so')


class MusicModule:

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = self.bot
            self.voice_states[server.id] = state
            return state

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        channel = ctx.message.author.voice_channel

        if channel is None:
            self.bot.say('You have to be in a voice channel in order to use this.')
            return False

        state = self.get_voice_state(ctx.message.server)

        state.voice = await self.bot.join_voice_channel(channel)
        return True

    @commands.command(pass_context=True, no_pm=True, name='play')
    async def play(self, ctx):
        self.bot.say('test')
        state = self.get_voice_state(ctx.message.server)
        self.bot.say('hi')
        try:
            self.bot.say('debug1')
            player = await state.voice.create_ytdl_player('https://www.youtube.com/watch?v=MGk-TdNpD5w')

            player.start()
        except Exception as e:
            self.bot.say(e)


def setup(bot):
    bot.add_cog(MusicModule(bot))
