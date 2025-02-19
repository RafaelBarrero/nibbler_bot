import difflib
import os
import discord
import random
import traceback
import time

from dotenv import load_dotenv

from typing import Tuple

from discord.ext import commands
from discord.ext.commands import Context

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

links = []

load_dotenv()


async def buscar_anime(ctx: Context, genero=None) -> Tuple[bool, bool]:
    global links
    message: discord.Message = ctx.message
    author: discord.Member = message.author
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
            print(d)
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


async def ver_link(ctx: Context, genero):
    message: discord.Message = ctx.message
    author: discord.Member = message.author
    devolver = []
    lin = [anime[1] if anime[0] == genero else None for anime in links]
    for link in lin:
        if link:
            devolver.append(link)
    response = random.choice(devolver)
    await ctx.send(f"Dúchate, Otaku culiado {author.mention}")
    await ctx.send(response)


class SearchAnime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='otaku', help='Te da un anime aleatorio según el género indicado')
    async def comprobar_anime(self, ctx: Context, genero=None):
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


async def setup(bot):
    await bot.add_cog(SearchAnime(bot))
