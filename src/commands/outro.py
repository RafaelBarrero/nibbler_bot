import discord
import pathlib

from discord.ext import commands
from discord.ext.commands import Context

from src.commands.play_sounds import PlaySound


class Outro(commands.Cog):
    file_path = pathlib.Path(__file__)
    sound_path = file_path.parent.parent.joinpath("canciones")

    def __init__(self, bot):
        self.bot = bot
        self.play = PlaySound(self.bot)

    @commands.command(name='outro', help='Vete con estilo fachero facherito')
    async def outro(self, ctx: Context):
        message: discord.Message = ctx.message
        author: discord.Member = message.author
        if author.voice:
            file = self.sound_path.joinpath("outro/outro.mp3")
            await self.play.play_sound(ctx, file)
            await author.move_to(None)
        else:
            await ctx.send("No te puedes ir si no has llegado, BOBO")


async def setup(bot):
    await bot.add_cog(Outro(bot))
