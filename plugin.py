import inspect
import logging


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class Plugin(object, metaclass=PluginMount):

    is_global = False
    fancy_name = None

    def __init__(self, client):
        self.client = client

    async def on_ready(self):
        pass

    async def _on_message(self, message, pfx):
        await self.on_message(message, pfx)

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_server_join(self, server):
        pass

    async def on_server_update(self, before, after):
        pass

    async def on_server_role_create(self, server, role):
        pass

    async def on_server_role_delete(self, server, role):
        pass

    async def on_server_role_update(self, server, role):
        pass

    async def on_voice_state_update(self, before, after):
        pass

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, member):
        pass

    async def on_typing(self, channel, user, when):
        pass
