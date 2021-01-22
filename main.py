# bot.py
import os
import random

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    guild_found = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild_found.name}(id: {guild_found.id})'
    )


@bot.command(name='99', help='Responde con una cita aleatoria de Brooklyn 99')
async def nine_nine(ctx):
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


@bot.command(name='c', help='Manda a una persona al canal de "Que me caigooo"')
async def caigo(ctx):
    mencion = ctx.message.mentions
    if len(mencion) == 0:
        await ctx.send("Menciona a alguien, cara de red")
    elif len(mencion) < 2:
        persona = ctx.message.mentions[0]
        canal_caida = discord.utils.get(ctx.guild.channels, name='Que me caigoooo')
        try:
            await persona.move_to(canal_caida)
            await ctx.send("TIRIRIRIRI. QUE ME CAIGOOOO")
        except discord.errors.HTTPException:
            await ctx.send(persona.mention + " no está, imbesil")
    else:
        await ctx.send("Menciona sólo a una persona, tonto")

bot.run(TOKEN)
