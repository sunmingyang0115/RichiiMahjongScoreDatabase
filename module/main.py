import discord
from bot import BotClient
import os

token = 'aminger'
with open(os.path.abspath("token.txt")) as file:
    token = file.read()

intents = discord.Intents.default()
intents.message_content = True
client = BotClient(intents=intents)
client.run(token)
