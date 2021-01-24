# bot.py
import os
import random

import discord
from discord.ext import commands
import keep_alive

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
guild_found = None


@bot.event
async def on_ready():
    global guild_found
    guild_found = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild_found.name}(id: {guild_found.id})'
    )

# Start server
keep_alive.keep_alive()


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
    rol_bol = False
    author = ctx.message.author
    mencion = ctx.message.mentions
    roles = guild_found.roles
    canal_caida = discord.utils.get(ctx.guild.channels, name='Que me caigoooo')
    if "everyone" in ctx.message.clean_content:
        await ctx.send("Te pensabas que podías tirar a todos pero NO")
        return
    if ctx.message.raw_role_mentions:
        role_id = ctx.message.raw_role_mentions[0]
        for rol in roles:
            if rol.id == role_id:
                rol_found = rol
                rol_bol = True
                break
    if author.voice:
        if len(mencion) == 0 and not rol_bol:
            await ctx.send("Menciona a alguien, cara de red")
        elif rol_bol:
            encontrados = False
            miembros = rol_found.members
            for miembro in miembros:
                if miembro.voice:
                    encontrados = True
                    await miembro.move_to(canal_caida)
            if not encontrados:
                await ctx.send(f"No hay nadie conectado de {rol_found.mention} :(")
            else:
                await ctx.send("TIRIRIRIRI. QUE ME CAIGOOOO")
        elif len(mencion) == 1:
            persona = ctx.message.mentions[0]
            try:
                await persona.move_to(canal_caida)
                await ctx.send("TIRIRIRIRI. QUE ME CAIGOOOO")
            except discord.errors.HTTPException:
                await ctx.send(f"{persona.mention} no está, imbesil")
        else:
            await ctx.send("Menciona sólo a una persona, tonto")
    else:
        await ctx.send("Entra al canal, COBARDE")


@bot.command(name='rafa', help='Responde si Rafa sigue vivo o no')
async def rafa(ctx):
    rafa_mention = '<@205283670209200129>'
    await ctx.send(f"{rafa_mention} sigue vivo :'c")


@bot.command(name='thanos', help='Comprueba si Thanos te ha matado o no')
async def thanos(ctx):
    author = ctx.message.author
    thanos_quote = [
        'Fuiste asesinado por Thanos, por el bien del universo :(',
        'Thanos te perdonó :D'
    ]

    response = random.choice(thanos_quote)
    await ctx.send(f"{author.mention} {response}")


@bot.command(name='d', help='Lanza un dado. Argumentos: Caras y número de veces')
async def roll_dice(ctx, *args):
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
        await ctx.send("Indica qué dado quieres tirar")

bot.run(TOKEN)

