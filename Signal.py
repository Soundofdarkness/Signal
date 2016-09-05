import discord
import logging
from discord.ext import commands
import asyncio
import sys
import traceback

description = 'Signal Bot Commands ! Warning xD'
logging.basicConfig(level=logging.INFO)


log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='signal.log', encoding='utf-8', mode='w')
log.addHandler(handler)

prefix = '?'
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await bot.send_message(ctx.message.author, 'This cannot be used in private Messages')
    elif isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.author, 'This command cannot be used currently')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)


@bot.event
async def on_ready():
    print('Signal Bot v1.0')
    print('------------------------')
    print('Username: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('Discord Version ' + discord.__version__)
    print('Author: Eleria')


@bot.event
async def on_resumed():
    print('Signal resumed')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

try:
    bot.load_extension(name='modules.MusicModule')
except Exception as e:
    print('Failed to load extension {}\n{}: {}'.format('InfoModule', type(e).__name__, e))


bot.run('MjA5NzcxOTg0Njk4MDgxMjgw.Cq7-FA.cl0SqTNZvp6ad4IfZuP0mzACX4M')

