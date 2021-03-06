import json

import pathlib
from discord.ext import commands
from discord.ext.commands import Context, has_permissions, MissingPermissions
from dropbox.files import WriteMode

from src.main import dbx


class ChangePrefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.PATH = pathlib.Path(__file__).parent.parent.parent

    @commands.command(name='prefijo', help='Cambia el prefijo')
    @has_permissions(administrator=True)
    async def prefix(self, ctx: Context, new_prefix: str):
        with open(f'{self.PATH}/prefixes.json', "wb") as f:  # Download prefixes from Dropbox
            metadata, res = dbx.files_download(path="/prefixes.json")
            f.write(res.content)

        with open(f'{self.PATH}/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = new_prefix

        with open(f'{self.PATH}/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        with open(f'{self.PATH}/prefixes.json', "rb") as f:  # Upload prefixes to Dropbox
            dbx.files_upload(f.read(), "/prefixes.json", mode=WriteMode('overwrite'))

        await ctx.send(f"Listo. Prefijo cambiado a \"{new_prefix}\" :D")

    @prefix.error
    async def prefix_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            mention = ctx.message.author.mention
            await ctx.send(f"Lo siento {mention}, no tienes permisos para eso :(")


def setup(bot):
    bot.add_cog(ChangePrefix(bot))
