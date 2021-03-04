from discord.ext import commands
from discord.ext.commands import Context
import random


class NineNine(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='99', help='Responde con una cita aleatoria de Brooklyn 99')
    async def nine_nine(self, ctx: Context):
        brooklyn_99_quotes = [
            'I\'m the human form of the 💯 emoji.',
            'Bingpot!',
            (
                'Cool. Cool cool cool cool cool cool cool, '
                'no doubt no doubt no doubt no doubt.'
            ),
            'Title of you sex tape'
        ]
        response = random.choice(brooklyn_99_quotes)
        await ctx.send(response)


def setup(bot):
    bot.add_cog(NineNine(bot))
