import os
import sys

import glob
import json
import traceback

import discord
import pathlib as pathlib
from discord.ext import commands

import dropbox
from dropbox.files import WriteMode

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DROPBOX_TOKEN = os.getenv('DROPBOX_TOKEN')
GUILD = "SALAS BORRACHAS"
PATH = pathlib.Path(__file__).parent.parent
intents = discord.Intents.all()
guild_found: discord.Guild = None

dbx = dropbox.Dropbox(DROPBOX_TOKEN)

links = []


def when_mentioned_or_function(func):
    def inner(client, message):
        r = func(client, message)
        r = commands.when_mentioned(client, message) + [r]
        return r

    return inner


def get_prefix(client, message: discord.Message) -> str:
    with open(PATH.joinpath("prefixes.json"), 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


bot = commands.Bot(command_prefix=when_mentioned_or_function(get_prefix), case_insensitive=True, intents=intents)
bot.remove_command("help")


@bot.event
async def on_guild_join(guild: discord.Guild):
    with open(PATH.joinpath("prefixes.json"), "wb") as f:  # Download prefixes from Dropbox
        metadata, res = dbx.files_download(path="/prefixes.json")
        f.write(res.content)

    with open(PATH.joinpath("prefixes.json"), 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open(PATH.joinpath("prefixes.json"), 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open(PATH.joinpath("prefixes.json"), "rb") as f:  # Upload prefixes to Dropbox
        dbx.files_upload(f.read(), "/prefixes.json", mode=WriteMode('overwrite'))


@bot.event
async def on_guild_remove(guild: discord.Guild):
    with open(PATH.joinpath("prefixes.json"), "wb") as f:  # Download prefixes from Dropbox
        metadata, res = dbx.files_download(path="/prefixes.json")
        f.write(res.content)

    with open(PATH.joinpath("prefixes.json"), 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open(PATH.joinpath("prefixes.json"), 'w') as f:
        json.dump(prefixes, f, indent=4)

    with open(PATH.joinpath("prefixes.json"), "rb") as f:  # Upload prefixes to Dropbox
        dbx.files_upload(f.read(), "/prefixes.json", mode=WriteMode('overwrite'))


@bot.event
async def on_ready():
    global guild_found
    guild_found = discord.utils.find(lambda g: g.name == GUILD, bot.guilds)
    with open(PATH.joinpath("prefixes.json"), "wb") as f:  # Download prefixes from Dropbox
        metadata, res = dbx.files_download(path="/prefixes.json")
        f.write(res.content)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild_found.name}(id: {guild_found.id})'
    )
    await bot.change_presence(activity=discord.Game(name=f"Cagar materia oscura"))


if __name__ == '__main__':
    file_path = pathlib.Path(__file__).parent.absolute()
    command_path = file_path.joinpath(file_path, "commands")
    help_path = file_path.joinpath(file_path, "help")
    command_files = glob.glob(f'{command_path}/*.py')
    help_files = glob.glob(f'{help_path}/*.py')
    files = command_files + help_files

    for file in files:
        if "init" not in file and "anime" not in file:
            file_name = pathlib.Path(file).name[:-3]
            try:
                if "help" in str(pathlib.Path(file)):
                    bot.load_extension(f"help.{file_name}")
                else:
                    bot.load_extension(f"commands.{file_name}")
            except Exception as e:
                print(f'Failed to load extension {file_name}.', file=sys.stderr)
                traceback.print_exc()

    bot.run(TOKEN)
