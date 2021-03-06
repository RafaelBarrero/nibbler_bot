import discord
import pathlib
from discord.ext import commands

from src.commands.play_sounds import PlaySound


class NoEsUnJuego(commands.Cog):
    # file_path = pathlib.Path(__file__)
    # sound_path = file_path.parent.parent.joinpath("canciones")

    def __init__(self, bot):
        self.bot = bot
        # self.play = PlaySound(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if any(word in message.content.lower() for word in ['esto es un juego', 'es esto un juego', 'es un juego',
                                                            'esto no es un juego']):

            await message.channel.send("https://pbs.twimg.com/media/Er4j_fcW4AMnEq2?format=jpg&name=360x360")
            await message.channel.send("***No te confundas, esto no es un juego***")

            # if message.author.voice:
            #     ctx = await self.bot.get_context(message)
            #     file = self.sound_path.joinpath("dance/song.mp3")
            #     await self.play.play_sound(ctx, file)

        # await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(NoEsUnJuego(bot))
