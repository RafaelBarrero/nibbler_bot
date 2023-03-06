import discord
import pathlib
from discord.ext import commands

from src.commands.play_sounds import PlaySound


class Gitano100(commands.Cog):
    file_path = pathlib.Path(__file__)
    sound_path = file_path.parent.parent.joinpath("canciones")

    def __init__(self, bot):
        self.bot = bot
        self.play = PlaySound(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        ctx = await self.bot.get_context(message)
        if any(word in message.content.lower() for word in ['tienen miedo']):
            file = self.sound_path.joinpath("gitano/miedo.mp3")
        elif any(word in message.content.lower() for word in ['quieres 50 euro', 'quiere cincuenta euro',
                                                              'quiere 50 euro', 'quiereh cincuentah euroh',
                                                              'quiereh 50 euro', '50 euroh']):
            file = self.sound_path.joinpath("gitano/euro.mp3")
        else:
            return
        await self.play.play_sound(ctx, file)


async def setup(bot):
    await bot.add_cog(Gitano100(bot))
