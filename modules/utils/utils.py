from config import Owner_ID as ident
from discord.ext import commands


def is_owner_check(message):
    return message.author.id == ident


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


