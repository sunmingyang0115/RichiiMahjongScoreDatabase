import discord
import csv

token = 'aminger'
with open('token.txt') as file:
    token = file.read()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

        #1231232 321 312
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(token)