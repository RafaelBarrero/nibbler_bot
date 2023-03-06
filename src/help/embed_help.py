import discord
from discord.ext import commands
from discord.ext.commands import Context, has_permissions, MissingPermissions

from src.main import get_prefix, GUILD


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx: Context):
        guild_borracheras = discord.utils.find(lambda g: g.name == GUILD, self.bot.guilds)
        author: discord.Member = ctx.message.author
        admin = author.guild_permissions.administrator
        em = discord.Embed(title="Help",
                           description=f"Lista de los comandos disponibles.\n\n"
                                       f"Usa {get_prefix(self.bot, ctx.message)}help <comando> para más información "
                                       f"sobre el comando.\n\n"
                                       f"**Prefijo actual**: {get_prefix(self.bot, ctx.message)}\n",
                           color=0x51007a)
        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}99",
                     value="Responde con una cita aleatoria de Brooklyn 99.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        if ctx.guild == guild_borracheras:
            em.add_field(name=f"{get_prefix(self.bot, ctx.message)}c <persona> ó <rol>",
                         value="Manda a una persona (o a todas las personas de un rol) al canal de \"Que me caigoooo\"."
                         , inline=False)

            em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}d <caras> <veces>",
                     value="Lanza un dado de las caras indicadas, el número de veces indicado.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}dance",
                     value="Reproduce: WOW, YOU COULD REALLY DANCE.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}help",
                     value="Muestra esta ayuda.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="_Esto no es un juego_",
                     value="Si te piensas que esto es un juego, estás equivocado. \nPregúntale a Lebron James si para "
                           "él es un juego.",
                     inline=False)

        if admin:
            em.add_field(name='** **', value="** **", inline=False)

            em.add_field(name=f"{get_prefix(self.bot, ctx.message)}prefijo <nuevo prefijo>",
                         value="Cambia el prefijo actual por el nuevo indicado.",
                         inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}rafa",
                     value="Responde si Rafa sigue vivo o no.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}thanos",
                     value="Comprueba si Thanos ha hecho lo mejor que podía hacer y te ha matado, o no.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}VOX",
                     value="Demuestra que eres un ESPAÑOL de verdad con este audio.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name=f"{get_prefix(self.bot, ctx.message)}presi",
                     value="Un audio aleatorio de tu presidente favorito.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        await ctx.send(embed=em)

        em2 = discord.Embed(color=0x51007a)
        em2.set_thumbnail(url=self.bot.user.avatar)

        em2.add_field(name=f"{get_prefix(self.bot, ctx.message)}fu <persona> <mensaje>",
                     value="Dime a quien imitar, dime lo que quieras que diga y te lo diré.",
                     inline=False,)

        await ctx.send(embed=em2)

    @help.command(name="99")
    async def nine_nine(self, ctx: Context):
        em = discord.Embed(title="99",
                           description="Responde con una cita aleatoria de Brooklyn 99.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}99.",
                     inline=True)

        await ctx.send(embed=em)

    @help.command(name="c")
    async def caigo(self, ctx: Context):
        guild_borracheras = discord.utils.find(lambda g: g.name == GUILD, self.bot.guilds)
        if ctx.guild == guild_borracheras:
            em = discord.Embed(title="C",
                               description="Manda a una persona (o a todas las personas de un rol) al canal de "
                                           "\"Que me caigoooo\".",
                               color=0x51007a)

            em.set_thumbnail(url=self.bot.user.avatar)

            em.add_field(name='** **', value="** **", inline=False)

            em.add_field(name="Sintaxis",
                         value=f"Escribe {get_prefix(self.bot, ctx.message)}c <persona> ó <rol>.",
                         inline=False)

            em.add_field(name='** **', value="** **", inline=False)

            em.add_field(name="Argumentos",
                         value="**<persona>**: Mención de la persona que quieres que se caiga.\n\n"
                               "**<rol>**: Mención del rol al que pertenecen las personas que quieres que se "
                               "caigan", inline=False)

            await ctx.send(embed=em)

    @help.command(name="d")
    async def roll_dice(self, ctx: Context):
        em = discord.Embed(title="D",
                           description="Lanza un dado y devuelve el resultado.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}d <caras> <veces>.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Argumentos",
                     value="**<caras>**: Lanza un dado una vez con las caras indicadas.\n\n"
                           "**<veces>**: Indica las veces que quieres lanzar el dado con las caras definidas (hasta un "
                           "máximo de 50 veces).",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="dance")
    async def dance(self, ctx: Context):
        em = discord.Embed(title="Dance",
                           description="Reproduce: WOW, YOU COULD REALLY DANCE.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}dance.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="help")
    async def help_help(self, ctx: Context):
        em = discord.Embed(title="Help",
                           description="Muestra la ayuda general con todos los comandos disponibles.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}help.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="lebron")
    async def lebron(self, ctx: Context):
        em = discord.Embed(title="_Esto no es un juego_",
                           description="Si te piensas que esto es un juego, estás equivocado. \n"
                                       "Pregúntale a Lebron James si para él es un juego.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value="El bot lee si te lo estas tomando como un juego.\n\n"
                           "Siempre acechando, siempre con mentalidad de tiburão glu glu glu.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="prefijo")
    @has_permissions(administrator=True)
    async def prefix(self, ctx: Context):
        em = discord.Embed(title="Prefijo",
                           description="Cambia el prefijo actual por el nuevo indicado.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}prefijo <nuevo prefijo>.",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Argumentos",
                     value=f"**<nuevo prefijo>**: Prefijo nuevo que quieres establecer para el bot.",
                     inline=False)

        await ctx.send(embed=em)

    @prefix.error
    async def prefix_error(self, ctx: Context, error):
        if isinstance(error, MissingPermissions):
            mention = ctx.message.author.mention
            await ctx.send(f"Lo siento {mention}, no tienes permisos para eso :(")

    @help.command(name="rafa")
    async def rafa(self, ctx: Context):
        em = discord.Embed(title="Rafa",
                           description="Responde si Rafa sigue vivo o no.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}rafa.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="thanos")
    async def thanos(self, ctx: Context):
        em = discord.Embed(title="Thanos",
                           description="Comprueba si Thanos ha hecho lo mejor que podía hacer y te ha matado, o no."
                                       "\n\nSi no lo ha hecho, debería hacerlo.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}thanos.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="vox")
    async def vox(self, ctx: Context):
        em = discord.Embed(title="VOX",
                           description="Demuestra que eres un ESPAÑOL de verdad con este audio.\n\n"
                                       "Es más, demuestra al chat que eres un ESPAÑOL de los de verdad, de los que "
                                       "apenas quedan.\n\n"
                                       "FRANCO, FRANCO. ¡VIVA ESPAÑA! ¡YO SOY ESPAÑOL, ESPAÑOL, ESPAÑOL!",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}VOX. Porque las cosas ESPAÑOLAS tienen que ir "
                           f"en mayúscula.",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="presi")
    async def presi(self, ctx: Context):
        em = discord.Embed(title="Presi",
                           description="Un audio aleatorio de tu presidente favorito.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}presi",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="dog")
    async def dog(self, ctx: Context):
        em = discord.Embed(title="El perro de la sabiduría",
                           description="El perro de la sabiduría te mostrará el camino a la verdad.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}dog",
                     inline=False)

        await ctx.send(embed=em)

    @help.command(name="fu")
    async def fakeyou(self, ctx: Context):
        em = discord.Embed(title="FakeYou",
                           description="Dime a quien imitar, dime lo que quieras que diga y te lo diré.",
                           color=0x51007a)

        em.set_thumbnail(url=self.bot.user.avatar)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Sintaxis",
                     value=f"Escribe {get_prefix(self.bot, ctx.message)}fu <persona> <mensaje>",
                     inline=False)

        em.add_field(name='** **', value="** **", inline=False)

        em.add_field(name="Argumentos",
                     value="**<persona>**: Persona a la que voy a imitar.\n\n"
                           "**<mensaje>**: Mensaje que quieres que diga.",
                     inline=False)

        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Help(bot))
