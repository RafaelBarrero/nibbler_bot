import asyncio
import glob
import os
import random

import discord
import pathlib
from discord.ext import commands
from discord.ext.commands import Context
from dotenv import load_dotenv

load_dotenv()
FFMPEG_PATH = os.getenv('FFMPEG_PATH')
DEV = (os.getenv('DEBUG', 'False') == 'True')


class PlaySound(commands.Cog):
    file_path = pathlib.Path(__file__)
    sound_path = file_path.parent.parent.joinpath("canciones")

    def __init__(self, bot):
        self.bot = bot

    async def play_sound(self, ctx: Context, path: pathlib.Path):
        author: discord.Member = ctx.message.author
        if author.voice:
            voice_channel: discord.VoiceChannel = author.voice.channel
        else:
            await ctx.send("Entra en un canal, tonto, que eres tonto")
            return

        if DEV:
            audio_source = discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=path)
        else:
            audio_source = discord.FFmpegPCMAudio(source=path)

        await voice_channel.connect()
        voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice.is_playing():
            voice.play(audio_source, after=None)
            if "vox" in str(path):
                await ctx.send(":flag_es:")
            elif "illojuan" in str(path):
                await ctx.send(":flag_ng:")
            while voice.is_playing():
                await asyncio.sleep(1)
            await voice.disconnect()
            print("terminó de reproducir el audio")

    @commands.command(name='stop', help='Termina el audio actual')
    async def stop(self, ctx: Context):
        voice: discord.VoiceClient = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()

    @commands.command(name='presi', help='ALÓ, PRESIDENTE')
    async def presi(self, ctx: Context):
        file_path = pathlib.Path(__file__).parent.parent.absolute()
        illojuan_path = file_path.joinpath(file_path, "canciones", "illojuan")
        illojuan_files = glob.glob(f'{illojuan_path}/*.mp3')
        illojuan_file = os.path.basename(random.choice(illojuan_files))
        file = self.sound_path.joinpath(f"illojuan/{illojuan_file}")

        await self.play_sound(ctx, file)

    @commands.command(name='vox', help='FRANCO, FRANCO. ESPAÑA, ESPAÑA')
    async def vox(self, ctx: Context):
        file = self.sound_path.joinpath("vox/song.mp3")

        await self.play_sound(ctx, file)

    @commands.command(name='dance', help='WOW, YOU CAN REALLY DANCE')
    async def dance(self, ctx: Context):
        file = self.sound_path.joinpath("dance/song.mp3")

        await self.play_sound(ctx, file)


def setup(bot):
    bot.add_cog(PlaySound(bot))
