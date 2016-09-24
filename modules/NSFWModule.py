from discord.ext import commands
import requests
import xml.etree.ElementTree as ET
from random import randrange
from modules.utils.utils import is_owner


class NSFWModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help='Rule34... aka Lewd')
    async def rule34(self, *tags: str):
        payload = {
            "limit": 100,
            "tags": " ".join(tags)
        }
        r34 = requests.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index", params=payload)
        root = ET.fromstring(r34.text)
        try:
            selected_post = root[randrange(len(root))]

            await self.bot.say("""{}
<http://rule34.xxx/index.php?page=post&s=view&id={}>""".format(
                "http:{}".format(selected_post.attrib["file_url"]),
                selected_post.attrib["id"]
        ))
        except (IndexError, ValueError):
            await self.bot.say("No results.")


def setup(bot):
    bot.add_cog(NSFWModule(bot))
