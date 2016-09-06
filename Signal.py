import discord
import logging
from discord.ext import commands
from config import Token as tkn
from config import Owner_ID as ident
from config import Modules as modules

logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='signal.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

bot = commands.Bot(command_prefix='?', description='Signal Bot by Eleria', pm_help=None)


@bot.event
async def on_ready():
    print('Signal started.')
    print('---------------')
    print('      Info     ')
    print('---------------')
    print('     BotName   ')
    print(bot.user.name)
    print('       ID      ')
    print(bot.user.id)
    print('   Owner ID    ')
    print(ident)
    print('---------------')
    print('     Author    ')
    print('  Eleria #5798 ')
    print('---------------')
    print('Discord Version')
    print(discord.__version__)
    print('---------------')


@bot.event
async def on_command(ctx):
    message = ctx.message
    destination = None
    if message.channel.is_private:
        destination = 'Private Message'
    else:
        destination = '#{0.channel.name} ({0.server.name})'.format(message)

    logger.info('{0.timestamp}: {0.author.name} in {1}: {0.content}'.format(message, destination))


@bot.event
async def on_message(message):
    bot.process_commands(message)

for module in modules:
    try:
        bot.load_extension(module)
        print('Loaded :' + module)
        logger.info('Loaded :' + module)
    except Exception as e:
        print('Failed to load extension {}\n{}: {}'.format(module, type(e).__name__, e))
        logger.info('Failed to load extension {}\n{}: {}'.format(module, type(e).__name__, e))

bot.run(tkn)
