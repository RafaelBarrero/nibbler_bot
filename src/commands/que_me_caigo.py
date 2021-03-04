import discord
from discord.ext import commands
from discord.ext.commands import Context


class QueMeCaigo(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='c', help='Manda a una persona al canal de "Que me caigooo"')
    async def caigo(self, ctx: Context):
        message: discord.Message = ctx.message
        rol_bol = False
        author: discord.Member = message.author
        mencion = message.mentions
        roles = message.guild.roles
        canal_caida: discord.VoiceChannel = discord.utils.get(ctx.guild.channels, name='Que me caigoooo')
        if "everyone" in message.clean_content:
            await ctx.send("Te pensabas que podías tirar a todos pero NO")
            return
        if message.raw_role_mentions:
            role_id = message.raw_role_mentions[0]
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
                miembro: discord.Member
                for miembro in miembros:
                    if miembro.voice:
                        encontrados = True
                        await miembro.move_to(canal_caida)
                if not encontrados:
                    await ctx.send(f"No hay nadie conectado de {rol_found.mention} :(")
                else:
                    await ctx.send("TIRIRIRIRI. QUE ME CAIGOOOO")
            elif len(mencion) == 1:
                persona: discord.Member = message.mentions[0]
                try:
                    await persona.move_to(canal_caida)
                    await ctx.send("TIRIRIRIRI. QUE ME CAIGOOOO")
                except discord.errors.HTTPException:
                    await ctx.send(f"{persona.mention} no está, imbesil")
            else:
                await ctx.send("Menciona sólo a una persona, tonto")
        else:
            await ctx.send("Entra al canal, COBARDE")


def setup(bot):
    bot.add_cog(QueMeCaigo(bot))
