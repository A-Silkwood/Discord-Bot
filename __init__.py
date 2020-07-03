import discord
import json
import asyncio


class Bot(discord.Client):
    def __init__(self):
        super(Bot, self).__init__()
        """Change bot data in the JSON file"""
        bot_data = json.load(open('bot_data.json'))
        self._token = bot_data.get('token')
        self._client_id = bot_data.get('client_id')
        self._owner_id = int(bot_data.get('owner_id'))
        self.prefix = bot_data.get('prefix')
        self.voice_client = None
        self.run(self._token)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        """Ignore Cases"""
        if message.author.bot:
            return

        if not message.content.startswith(self.prefix):
            return

        """Grabs command and arguments"""
        user_input = message.content[len(self.prefix):].split(' ')
        command = user_input[0]
        args = user_input[1:]

        """Commands"""
        async def invite():
            link = discord.utils.oauth_url(self._client_id, discord.Permissions(8))
            await message.channel.send(f"Here's my invite link: {link}")

        async def join():
            try:
                channel = message.author.voice.channel
            except AttributeError:
                username = message.author.nick if message.author.nick is not None else message.author.display_name
                await message.channel.send(f'Sorry {username}, you are not in a channel')
                return

            try:
                if self.voice_client is not None and self.voice_client.channel.id != channel.id:
                    await self.voice_client.disconnect()
                self.voice_client = await channel.connect()
            except asyncio.TimeoutError:
                pass
            except discord.errors.ClientException:
                pass
            except discord.opus.OpusNotLoaded:
                print('Opus library not loaded')
            return

        async def leave():
            if self.voice_client is not None:
                await self.voice_client.disconnect()
                self.voice_client = None

        async def stop():
            if message.author.id == self._owner_id:
                await leave()
                await self.close()

        commands = {
            'inv': invite,
            'invite': invite,
            'join': join,
            'leave': leave,
            'close': stop,
            'quit': stop,
            'stop': stop
        }

        """Execute command"""
        func = commands.get(command)
        try:
            await func()
        except TypeError:
            pass


discord_bot = Bot()
