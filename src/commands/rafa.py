from discord.ext import commands
from discord.ext.commands import Context


class Rafa(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rafa', help='Responde si Rafa sigue vivo o no')
    async def rafa(self, ctx: Context):
        rafa_mention = '<@205283670209200129>'
        await ctx.send(f"{rafa_mention} sigue vivo :'c")


def setup(bot):
    bot.add_cog(Rafa(bot))
