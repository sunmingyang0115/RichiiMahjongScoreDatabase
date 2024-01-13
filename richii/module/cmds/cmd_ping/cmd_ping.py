import discord


async def on_cmd_ping(self, message, frags):
    await message.channel.send('pong')