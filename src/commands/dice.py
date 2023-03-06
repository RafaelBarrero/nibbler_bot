from discord.ext import commands
from discord.ext.commands import Context
import random


class Dice(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='d', help='Lanza un dado. Argumentos: Caras y número de veces')
    async def roll_dice(self, ctx: Context, *args):
        count = 1
        if args:
            dice = int(args[0])
            if len(args) == 2:
                tries = (int(args[1]) if int(args[1]) <= 50 else 50)
            else:
                tries = 1
            number_list = []
            while count <= tries:
                number = random.randint(1, dice)
                number_list.append(number)
                count += 1
            str_number = ', '.join([f"{number}" for number in number_list])
            await ctx.send(str_number)
        else:
            await self.roll_dice(ctx, 6)


async def setup(bot):
    await bot.add_cog(Dice(bot))
