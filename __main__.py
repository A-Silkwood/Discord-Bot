from discord.ext import commands
from discord.ext.commands import errors
import os
import json

client = commands.Bot(command_prefix='>')
data = json.load(open('bot_data.json'))
_token = data.get('token')


@client.event
async def on_ready():
    print(f'{client.user} is ready')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong: {round(client.latency * 1000)}ms')


"""Cogs"""


@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}', delete_after=3)
        print(f'{ctx.author} loaded {extension}')
    except errors.ExtensionAlreadyLoaded:
        await ctx.send(f'{extension} was already loaded', delete_after=3)
        print(f'{extension} was already loaded')
    except errors.ExtensionNotFound:
        await ctx.send(f'{extension} was not found', delete_after=3)
        print(f'{extension} was not found')


@client.command()
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}', delete_after=3)
        print(f'{ctx.author} reloaded {extension}')
    except errors.ExtensionNotLoaded:
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}', delete_after=3)
        print(f'{ctx.author} loaded {extension}')


@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}', delete_after=3)
        print(f'{ctx.author} unloaded {extension}')
    except errors.ExtensionNotLoaded:
        await ctx.send(f'{extension} is not loaded', delete_after=3)
        print(f'{extension} is not loaded')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

client.run(_token)
