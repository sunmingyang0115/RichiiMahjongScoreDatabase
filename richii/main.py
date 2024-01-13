import discord
from module.bot import BotClient

token = 'aminger'
with open('~/../token.txt') as file:
    token = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = BotClient(intents=intents)
client.run(token)