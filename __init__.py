import discord

client = discord.Client()
_client_id = '365981597276700672'
_token = 'MzY1OTgxNTk3Mjc2NzAwNjcy.Xv4NSQ.BpzWQ2d2wN2Ox1Peiucb2npPHiQ'
prefix = '>'


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

    async def invite():
        link = discord.utils.oauth_url(_client_id, discord.Permissions(8))
        await message.channel.send(f"Here's my invite link: {link}")

    async def invalid_command():
        print(command, args)

    commands = {
        'inv': invite,
        'invite': invite
    }

    func = commands.get(command, invalid_command)
    await func()


client.run(_token)
