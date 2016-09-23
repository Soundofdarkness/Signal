from config import Owner_ID as ident
from discord.ext import commands
import random
import os, platform


def is_owner_check(message):
    return message.author.id == ident


def is_owner():
    return commands.check(lambda ctx: is_owner_check(ctx.message))


def ranint(i1: int, i2:int):
    r1 = random.getrandbits(10)
    random.seed(r1)
    out = random.randint(i1, i2)
    return out

def ping(host):
    # Ping parameters as function of OS
    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0
