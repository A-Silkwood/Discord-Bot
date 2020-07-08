import discord
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        print(f'{ctx.author} kicked {member}\nReason: {reason}')

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        print(f'{ctx.author} banned {member}\nReason: {reason}')

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                print(f'{ctx.author} unbanned {user}')
                return

    @commands.command()
    async def clear(self, ctx, *args):
        if len(args) == 1:
            try:
                amount = int(args[0])
                if amount > 0:
                    await ctx.channel.purge(limit=amount + 1)
                    await ctx.send(f'Deleted {amount} message(s)!', delete_after=3)
                    print(f'{ctx.author} deleted {amount} messages')
            except ValueError:
                pass


def setup(client):
    client.add_cog(Admin(client))
