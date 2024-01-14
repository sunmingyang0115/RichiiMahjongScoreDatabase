from cmds.cmd_db.cmd_db_util import command_fetch, command_store2


async def on_cmd_db_store(self, message, frags):
    await command_store2(frags, str(message.id), self.db)
    await message.add_reaction('✅')


async def on_cmd_db_get(self, message, frags):
    # frags[3] is user id
    usr = await command_fetch(frags, self.db)
    out = ''
    for e in usr:
        out = out + str(e) + "\n"
    await message.channel.send(out)