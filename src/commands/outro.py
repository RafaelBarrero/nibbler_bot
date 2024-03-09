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
        mentions = message.mentions
        admin = author.guild_permissions.administrator
        if author.voice:
            file = self.sound_path.joinpath("outro/outro.mp3")
            await self.play.play_sound(ctx, file)
            if len(mentions) == 0:
                await author.move_to(None)
            elif len(mentions) > 0 and admin:
                author_in_mentions = author.mention in [mention.mention for mention in mentions]
                mention_list = [mention for mention in mentions if mention.mention != author.mention]
                if author_in_mentions and len(mention_list) > 0:
                    await ctx.send(f"{author.mention} ha decidido irse de orgía con "
                                   f"{', '.join([mention.mention for mention in mention_list])}")
                elif not author_in_mentions and len(mention_list) > 0:
                    vaya = 'vaya'
                    if len(mention_list) > 1:
                        vaya += 'n'
                    await ctx.send(f"{author.mention} quiere que " 
                                   f"{', '.join([mention.mention for mention in mentions])} se {vaya} de orgía gay")
                for mention in mentions:
                    persona: discord.Member = mention
                    await persona.move_to(None)
            elif len(mentions) > 0 and not admin:
                await ctx.send("No tienes permisos, tonto. Ahora te vas tú solito")
                await author.move_to(None)
        else:
            await ctx.send("No te puedes ir si no has llegado, BOBO")


async def setup(bot):
    await bot.add_cog(Outro(bot))
