import discord
from datetime import datetime

async def get_simple_embed(bot, channel, title, content):
    embed = discord.Embed(title=title, colour=0xf0ccc4, timestamp=datetime.now())
    for x in content:
        embed.add_field(name='', value=x, inline=False)
    embed.set_footer(text=bot.user.name, icon_url=bot.user.display_avatar.url)
    await channel.send(embed=embed)

async def get_complicated_embed(bot, channel, title, content):
    pass
