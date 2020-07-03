import discord
import json

client = discord.Client()
"""Change bot data in the JSON file"""
_bot_data = json.load(open('bot_data.json'))
_token = _bot_data.get('token')
_client_id = _bot_data.get('client_id')
prefix = _bot_data.get('prefix')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    """Ignore Cases"""
    if message.author.bot:
        return

    if not message.content.startswith(prefix):
        return

    """Grabs command and arguments"""
    command = message.content[1:].split(' ')[0]
    args = message.content[1:].split(' ')[1:]

    """Commands"""
    async def invite():
        link = discord.utils.oauth_url(_client_id, discord.Permissions(8))
        await message.channel.send(f"Here's my invite link: {link}")

    async def search():
        print('searching')

    commands = {
        'inv': invite,
        'invite': invite,
        'search': search
    }

    """Execute command"""
    func = commands.get(command)
    try:
        await func()
    except TypeError:
        pass


client.run(_token)
