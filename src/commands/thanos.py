import discord
from discord.ext import commands
from discord.ext.commands import Context
import random


class Thanos(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='thanos', help='Comprueba si Thanos te ha matado o no')
    async def thanos(self, ctx: Context):
        message: discord.Message = ctx.message
        author: discord.Member = message.author
        thanos_quote = [
            'Fuiste asesinado por Thanos, por el bien del universo :(',
            'Thanos te perdonó :D'
        ]

        response = random.choice(thanos_quote)
        await ctx.send(f"{author.mention} {response}")


def setup(bot):
    bot.add_cog(Thanos(bot))
