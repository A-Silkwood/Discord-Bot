from discord.ext import commands
import random


class Minigames(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *question):
        responses = ['It is certain',
                     'It is decidedly so',
                     'Without a doubt',
                     'Yes - definitKely',
                     'You may rely on it',
                     'As I see it, yes',
                     'Most likely',
                     'Outlook good',
                     'Yes',
                     'Signs point to yes',
                     'Reply hazy, try again',
                     'Ask again later',
                     'Better not tell you now',
                     'Cannot predict now',
                     'Concentrate and ask again',
                     "Don't count on it",
                     'My reply is no',
                     'My sources say no',
                     'Outlook not so good',
                     'Very doubtful']
        if len(question) > 0:
            await ctx.send(f'Question: {" ".join(question)}\nAnswer: {random.choice(responses)}')


def setup(client):
    client.add_cog(Minigames(client))
