import discord
from discord.ext import commands
import youtube_dl
import urllib.request
from Mod import re
'''
Por conta de eu  ter baixado a parte a biblioteca re.
O "from Mod import re" foi necessário na minha maquina.
Mas na teoria a biblioteca faz parte da versão padrão do Python.
E só precisaria escrever "import re".
'''



class comandos(commands.Cog):
    def _init_(self, client):
        self.client = client
    @commands.command(name="stc", help="Comando simples para saber se o Bot está respondendo")
    async def boas_vindas(self, ctx):
        resp = "Pai ta ON"
        await ctx.send(resp)
    @commands.command(name="entra", help="Identifca e entra no canal de Voz do autor da menssagem")
    async def connect(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
    @commands.command(name="vaza", help="Sai do canal de Voz em que está")
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send('Não estou em nenhum canal')
        else:
            await ctx.voice_client.disconnect()
    @commands.command(name="toca", help="Toca uma musica através de seu título, pesquisado no youtube")
    async def tocar(self, ctx, *text):
        titulos = []
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["1", "2", "3", "4", "5"]
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        search_keyword = (' '.join(text))
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword.replace(' ', '+'))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        video_ids = list(set(video_ids))
        ydl_opts = {'outtmpl': '%(title)s',}
        for video_id in video_ids:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(('https://www.youtube.com/watch?v='+str(video_id)), download=False)
                titulo = info['title']
                titulos.append(titulo)
                if len(titulos) == 5:
                    break
        for titulo in titulos:
            await ctx.send('{:2} {}'.format((titulos.index(titulo)+1), titulo))
        await ctx.send("Escolha entre 1, 2, 3, 4 ou 5")
        try:
            msg = await client.wait_for("message", check=check, timeout=10)
            m = msg.content.lower()
            #m = '1'
            #except asyncio.TimeoutError:
        except:
            await ctx.send("ERRO, tocando música 1")
            m = 1
        await ctx.send("Você escolheu "+ str(m))
        musica = titulos.pop((int(m)-1))
        musica2 = video_ids.pop((int(m)-1))
        print(musica)
        print(musica2)
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max ','options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio/best'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            url = 'https://www.youtube.com/watch?v='+ musica2
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
            voice = ctx.voice_client
            await ctx.send("Tocando " + musica)
            voice.play(source)
    @commands.command(name="url", help="Toca uma musica através de sua URL, pesquisada no youtube")
    async def playu(self, ctx, url):
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max ', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio/best'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
            voice = ctx.voice_client
            await ctx.send("Tocando " + url)
            voice.play(source)
    @commands.command(name="tira", help="Retira da música que estiver tocando")
    async def tirar(self, ctx):
        voice = ctx.voice_client
        voice.stop()
        await ctx.send("Música retirada")
    @commands.command(name="pare", help="Para a música que estiver tocando")
    async def parar(self, ctx):
        voice = ctx.voice_client
        if voice.is_playing():
            voice.pause()
            await ctx.send("Tô parado")
        else:
            await ctx.send("Não tem oque parar")
    @commands.command(name="continue", help="Continua a música parada")
    async def resume(self, ctx):
        voice = ctx.voice_client
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("Mas não tá parado")
def setup(client):
    client.add_cog(comandos(client))
