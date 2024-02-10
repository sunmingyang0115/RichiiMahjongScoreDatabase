import discord
from datetime import datetime

async def send_simple_embed(bot, channel, title, content):
    embed = discord.Embed(title=title, colour=0xf0ccc4, timestamp=datetime.now())
    for x in content:
        embed.add_field(name='', value=x, inline=False)
    embed.set_footer(text=bot.user.name, icon_url=bot.user.display_avatar.url)
    await channel.send(embed=embed)


# modifed simple embed for commands issued by @user
async def send_command_embed(bot, channel, content, command_name, isuser):
    content.append("Command issued by <@" + str(isuser.id) + ">")
    await send_simple_embed(bot, channel, command_name + " Command", content)

async def send_complicated_embed(bot, channel, title, content):
    pass
