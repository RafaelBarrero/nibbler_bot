import os
import fakeyou
from discord.ext import commands
from discord.ext.commands import Context, has_permissions
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import pathlib
from src.commands.play_sounds import PlaySound

load_dotenv()

FAKEYOU_EMAIL = Fernet(os.getenv('KEY')).decrypt(os.getenv('FAKEYOU_EMAIL')).decode()
FAKEYOU_PASSWORD = Fernet(os.getenv('KEY')).decrypt(os.getenv('FAKEYOU_PASSWORD')).decode()
DEV = (os.getenv('DEBUG', 'False') == 'True')


class FakeYou(commands.Cog):
    file_path = pathlib.Path(__file__)
    if DEV:
        sound_path = file_path.parent.parent.joinpath("fakeyou.wav")
    else:
        sound_path = file_path.parent.parent.parent.joinpath("fakeyou.wav")

    def __init__(self, bot):
        self.bot = bot
        self.session = None
        self.tts = fakeyou.AsyncFakeYou()
        self.play = PlaySound(self.bot)

    @commands.command(name='fu', help='Hablo con la voz que quieras, guapo')
    @has_permissions(administrator=True)
    async def fu(self, ctx: Context, *args):
        try:
            self.session = await self.tts.login(FAKEYOU_EMAIL, FAKEYOU_PASSWORD)
            await ctx.send("Buscando la voz")
            voice_to_search = args[0]
            text_to_say = ' '.join(args[1:])
            voice = await self.tts.search(voice_to_search)

            if len(voice.voices.ttsModelType):
                voice_token = voice.voices.modelTokens[0]
                file = self.sound_path
                await ctx.send("Esperando a que el notas me deje hablar")
                await self.tts.say(text_to_say, voice_token, filename="fakeyou.wav")
                await self.play.play_sound(ctx, file)
            else:
                await ctx.send("Te voy a matar. \nNo encuentro la voz que buscas.")
                return

            if not args:
                await ctx.send("Bobo, no sé a quien imitar")
                return

            if len(args) < 2:
                await ctx.send("Bobo, no sé que decir")
                return

        except (KeyboardInterrupt, RuntimeError, RuntimeWarning, Exception) as e:
            print(e)
            pass


def setup(bot):
    bot.add_cog(FakeYou(bot))
