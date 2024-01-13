from richii.module import db
from richii.module.cmds.cmd_db.cmd_db_util import command_store, command_fetch


async def on_cmd_db_store(self, message, frags):
    await command_store(frags, message.id, self.db)
    await message.add_reaction('✅')


async def on_cmd_db_get(self, message, frags):
    print(frags)
    # frags[3] is user id
    usr = await command_fetch(frags, self.db)
    out = ''
    for e in usr:
        out += e+'\n'
    await message.channel.send(out)