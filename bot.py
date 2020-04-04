# bot.py

import os
import discord
import pickle

DEFAULT_PASSWORD_CHANNEL_NAME = 'open-sesame'

DEFAULT_NP_ROLE = 'Needs Password'
DEFAULT_ROLE = 'Default Role'

TOKEN = os.environ['TOKEN']

# on setup
# create role "Needs Password"
# create role default (with same permission as setup karne vale ka)
# create channel "open-sesame" (only visible to Need Password)

# commands
# change password [password]
# change default role [default_role] (check if below)

class ServerData:
    def __init__(self, np_id=0, def_id=0, channel_id=0, pws='12345'):
        self.np_id = np_id
        self.def_id = def_id
        self.channel_id = channel_id
        self.pw = pws
    
    def __str__(self):
        return f'id: {self.np_id}, def_id: {self.def_id}, channel_id: {self.channel_id}, pw: {self.pw}'
    
    def print(self, guild):
        return f'NP_Role_Name: {guild.get_role(self.np_id)}, Default_Role_Name: {guild.get_role(self.def_id)}, Password_Channel_Name: {guild.get_channel(self.channel_id)}, Password: {self.pw}'


storage = {}
try:
    storage = pickle.load(open('serverdata', 'rb'))
except:
    pass

client = discord.Client()

async def initialSetup(message):
    g = message.guild
    ms = message.content.split()

    if len(ms) != 2:
        await message.channel.send(content='Invalid Parameters')
        return
    if g.id in storage:
        await message.channel.send(content='Already Initialised')
        return
    
    await message.channel.send(content='Initialising...')

    author_role = message.author.roles[len(message.author.roles)-1]
    
    def_role = await g.create_role(name = DEFAULT_ROLE, permissions = author_role.permissions)

    np_role = await g.create_role(name = DEFAULT_NP_ROLE, colour = discord.Colour.darker_grey())

    overwrites = {
        g.default_role: discord.PermissionOverwrite(create_instant_invite = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, add_reactions = False, read_messages = False, send_messages = False, send_tts_messages = False, manage_messages = False, embed_links = False, attach_files = False, read_message_history = False, mention_everyone = False, external_emojis = False),
        np_role: discord.PermissionOverwrite(create_instant_invite = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, add_reactions = False, read_messages = True, send_messages = True, send_tts_messages = False, manage_messages = False, embed_links = False, attach_files = False, read_message_history = False, mention_everyone = False, external_emojis = False),
        g.me: discord.PermissionOverwrite(create_instant_invite = True, manage_channels = True, manage_permissions = True, add_reactions = True, read_messages = True, send_messages = True, manage_messages = True, embed_links = True, read_message_history = True)
    }
    pw_channel = await g.create_text_channel(DEFAULT_PASSWORD_CHANNEL_NAME, position=0, overwrites=overwrites)
    storage[g.id] = ServerData(np_role.id, def_role.id, pw_channel.id, ms[1])        

    await message.delete()
    await message.channel.send(content='Done.')

    pickle.dump(storage, open('serverdata','wb'))

async def changeSetup(message):
    g = message.guild
    ms = message.content.split()

    if g.id not in storage:
        await message.channel.send(content='Bot not initialised')
        return

    if ms[1] == 'password' and len(ms) == 3:
        storage[g.id].pw = ms[2]
        await message.channel.send(content="Password successfully changed")
        await message.delete()
    elif ms[1] == 'default_role':
        name = message.content[message.content.find('default_role')+13:]
        role = discord.utils.get(g.roles, name=name)
        if role is not None and g.me.roles[-1]>role:
            storage[g.id].def_id = role.id
            await message.channel.send(content=f'Changed Default Role to {role.name}')
        else:
            await message.channel.send(content=f'Invalid Role {name}')
    elif ms[1] == 'np_role':
        name = message.content[message.content.find('np_role')+8:]
        role = discord.utils.get(g.roles, name=name)
        if role is not None and g.me.roles[-1]>role:
            storage[g.id].np_id = role.id
            await message.channel.send(content=f'Changed \'Needs Password\' role to {role.name}')
        else:
            await message.channel.send(content=f'Invalid Role {name}')
    elif ms[1] == 'channel' and len(ms) == 3:
        name = ms[2]
        channel = discord.utils.get(g.text_channels, name=name)
        if channel is not None:
            storage[g.id].channel_id = channel.id
            await message.channel.send(content=f'Changed password channel to {channel.name}')
        else:
            await message.channel.send(content='Invalid Channel')
    else:
        return
    
    pickle.dump(storage, open('serverdata','wb'))

async def generateHelp(message):

    content = """Hello
    Password Protect Server Bot enables you to password protect your server. This bot will make sure that a user coming online has to enter a passcode correctly before they can access it.
    Commands:
    pps!init [password]
        Initialises the bot. Add the role 'Needs Password' to the members who should enter a password before entering.
    pps!exit
        To manually logout of the server
    pps!change <password/default_role/np_role/channel> [new value]
        password: to change the password
        channel: to change the channel where you enter password
        default_role: to change the role assigned after authentication
        np_role:  to change the role given to members who enter a password before entering
    """
    await message.channel.send(content=content)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    # guild = discord.utils.get(client.guilds, name=GUILD)

    print(f'{client.user} is connected to the following guilds:')
    
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')
        if guild.id in storage:
            print(f'Guild config:\n{storage[guild.id].print(guild)}')
        else:
            print('Guild not configured yet')

    act = discord.Game("pps!help")
    await client.change_presence(activity=act)


@client.event
async def on_message(message):
    g = message.guild
    ms = message.content.split()

    # pps!setup
    if len(ms)>0:
        if ms[0] == 'pps!init':
            await initialSetup(message)
        elif ms[0] == 'pps!change':
            await changeSetup(message)
        elif ms[0] == 'pps!help':
            await generateHelp(message)

    if g.id in storage:
        if message.channel.id == storage[g.id].channel_id:
            if(message.content == storage[g.id].pw and discord.utils.get(message.author.roles, id=storage[g.id].np_id) is not None):
                await message.delete()    
                def_role = discord.utils.get(message.guild.roles, id=storage[g.id].def_id)
                if def_role is not None:
                    await message.author.add_roles(def_role)
                    print('added role')
                    await message.channel.send(content=f'You may enter {message.author.display_name}')
                else:
                    await message.channel.send(content='Invalid Configuration', delete_after=40.0)
            else:
                await message.delete()
    
        elif message.content == 'pps!exit':
            to_remove = discord.utils.get(message.author.roles, id=storage[g.id].def_id)
            if(to_remove is not None):
                await message.author.remove_roles(to_remove)
                print(f'Removed role')
            await message.delete()
    

@client.event
async def on_member_update(before, after):
    g = before.guild

    if g.id in storage and before.status != after.status:
        channel = g.get_channel(storage[g.id].channel_id)
        deleted = await channel.purge(limit=100, check=lambda m: m.author == client.user)
        if len(deleted)>0:
            print('Purged {} message(s)'.format(len(deleted)))

        if after.status == discord.Status.offline and discord.utils.get(after.roles, id=storage[g.id].np_id) is not None: #has np_role
                print(f'{before.display_name}[{g.name}] went offline')
                await after.remove_roles(discord.utils.get(g.roles, id=storage[g.id].def_id))
                print(f'Removed role')



client.run(TOKEN)

