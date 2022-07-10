import discord
from discord.ext import commands


class NoEsUnJuego(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if any(word in message.content.lower() for word in ['esto es un juego', 'es esto un juego', 'es un juego',
                                                            'esto no es un juego']):

            await message.channel.send("https://pbs.twimg.com/media/Er4j_fcW4AMnEq2?format=jpg&name=360x360")
            await message.channel.send("***No te confundas, esto no es un juego***")


def setup(bot):
    bot.add_cog(NoEsUnJuego(bot))
