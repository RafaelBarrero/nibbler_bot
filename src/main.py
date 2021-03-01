# bot.py
import difflib
import os
import random
import time
import traceback
from typing import Tuple
import youtube_dl

import discord
from discord.ext import commands

from dotenv import load_dotenv

from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = "SALA BORRACHERAS"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
guild_found = None

links = []


@bot.event
async def on_ready():
    global guild_found
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


async def buscar_anime(ctx, genero=None) -> Tuple[bool, bool]:
    global links

    author = ctx.message.author
    if genero:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),
                                  chrome_options=chrome_options)
        base = "https://www3.animeflv.net/"
        driver.delete_all_cookies()

        driver.get(f"{base}/browse")

        select = Select(driver.find_element_by_id('genre_select'))
        opciones = [opciones.text for opciones in select.options]
        close_match = difflib.get_close_matches(genero, opciones)

        if close_match:
            d = close_match[0]
            select.select_by_visible_text(d)

            WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, "btn"))).click()  # Boton filtrar
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.PARTIAL_LINK_TEXT, "Permitir todas")))  # Boton cookies
                time.sleep(0.5)
                driver.find_element_by_partial_link_text("Permitir todas").click()
            except:
                traceback.print_exc()
                pass

            while True:
                ul_animes = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "ListAnimes"))).find_elements_by_tag_name("li")
                lista = [[genero, anime.find_element_by_tag_name("a").get_attribute('href')] for anime in
                         ul_animes]
                links += lista

                WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "pagination")))  # Páginas

                ul_animes = driver.find_element_by_class_name("NvCnAnm").find_element_by_class_name("pagination")
                li_botones = ul_animes.find_elements_by_tag_name("li")
                siguiente = li_botones[-1].find_element_by_tag_name("a")

                if '#' in siguiente.get_attribute('href'):
                    print("HA LLEGADO AL FIN")
                    break
                else:
                    siguiente.click()
                    print("siguiente")

            driver.quit()
            print("termino")
            return True, True
        else:
            driver.quit()
            print("no esta ese genero")
            await ctx.send(f"No he encontrado animes con el género {genero}. "
                           f"Así te puedes duchar {author.mention}")
            return True, False
    else:
        rafa_mention = '<@205283670209200129>'
        await ctx.send(f"Error desconocido {rafa_mention}")


async def ver_link(ctx, genero):
    author = ctx.message.author
    devolver = []
    lin = [anime[1] if anime[0] == genero else None for anime in links]
    for link in lin:
        if link:
            devolver.append(link)
    response = random.choice(devolver)
    await ctx.send(f"Dúchate, Otaku culiado {author.mention}")
    await ctx.send(response)


@bot.command(name='otaku', help='Te da un anime aleatorio según el género indicado')
async def comprobar_anime(ctx, genero=None):
    if genero:
        lin = list(set([anime[0] for anime in links]))
        close_match = difflib.get_close_matches(genero, lin)
        if close_match:
            print("esta el genero")
            await ver_link(ctx, close_match[0])
        else:
            print("ejecutar script")
            await ctx.send(f"No hay links de {genero}. Buscando enlaces...")
            bien, ver = await buscar_anime(ctx, genero)
            if bien:
                if ver:
                    await ver_link(ctx, genero)
            else:
                rafa_mention = '<@205283670209200129>'
                await ctx.send(f"Error en buscar_anime {rafa_mention}")
    else:
        print("script contra toda la página")
        await ctx.send("Pero pon un género bro")


@bot.command(name='vox', help='FRANCO, FRANCO. ESPAÑA, ESPAÑA')
async def vox(ctx):
    author = ctx.message.author
    voice_channel = author.voice.channel
    heroku = "/app/src/canciones/vox/song.mp3"
    windows = "canciones/vox/song.mp3"

    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(source=heroku))
    time.sleep(23)
    await voice.disconnect()


@bot.command(name='dance', help='WOW, YOU CAN REALLY DANCE')
async def vox(ctx):
    author = ctx.message.author
    voice_channel = author.voice.channel
    heroku = "/app/src/canciones/dance/song.mp3"
    windows = "canciones/dance/song.mp3"

    await voice_channel.connect()
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(source=heroku))
    time.sleep(17)
    await voice.disconnect()

bot.run(TOKEN)
