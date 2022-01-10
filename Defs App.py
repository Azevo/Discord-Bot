import discord
from discord.ext import commands
import youtube_dl
import urllib.request
from Mod import re
import wikipedia

'''

-----------------------------------------------------------------------------------------------------

Por conta de eu  ter baixado a parte a biblioteca re.
O "from Mod import re" foi necessário na minha maquina.
Mas na teoria a biblioteca faz parte da versão padrão do Python.
E só precisaria escrever "import re".

----------------------------- Atualização do dia 10/01/2022 ------------------------------------------

Leia-se usuário como aquele que manda uma mensagem com o prefixo "!" em algum canal de mensagem, onde:
* O usuário é o author da mensagem.
* A mensagem é o comando + texto. 
* O canal de voz ou mensagem é o ctx (contexto).
* O cliente é o Bot.

-------------------------------------------------------------------------------------------------------

'''

class comandos(commands.Cog):
    def _init_(self, client):
        self.client = client
        
    # Comando para saber se o Bot está respondendo e também serve para avisar de novidades.
    @commands.command(name="news", help="Comando simples para saber se o Bot está respondendo")
    async def boas_vindas(self, ctx):
        resp = "Bot Funcionando, agora podendo escolher a música no 'toca' e novo comando 'wiki'"
        await ctx.send(resp) # Manda a mensagem no contexto (canal de mensagem) em que foi chamado o comando
        
    # Comando que identifica e conecta o Bot ao canal de voz do usuário.
    @commands.command(name="entra", help="Identifca e entra no canal de Voz do autor da menssagem")
    async def connect(self, ctx): # Cria uma função "connect" assíncrona (async), ou seja que pode ser chamada a qualquer momento
        if ctx.author.voice is None: # Se o canal de voz do usuário for nenhum:
            await ctx.send("Você não está em um canal") # Manda uma mensagem de alerta no contexto (canal de mensagem)
        elif ctx.voice_client is None: # Se o Bot não estiver em um canal de voz:
            voice_channel = ctx.author.voice.channel # Identifica o canal de voz do usuário
            await voice_channel.connect() # Conecta o Bot ao canal de voz do usuário
        else: # Senão, restando apenas a opção dele já estar em um canal de voz, mas não o do usuário
            voice_channel = ctx.author.voice.channel # Identifica o canal de voz do usuário
            await ctx.voice_client.move_to(voice_channel) # Move então o Bot para o canal de Voz do usuário 
            
    # Comando para tirar o Bot do canal de voz que estiver conectado.
    @commands.command(name="vaza", help="Sai do canal de Voz em que está")
    async def disconnect(self, ctx): # Cria uma função "disconnect" assíncrona (async), ou seja que pode ser chamada a qualquer momento
        if ctx.voice_client is None: # Se o Bot não estiver conectado a nenhum canal de voz:
            await ctx.send('Não estou em nenhum canal') # Manda uma mensagem de alerta no contexto (canal de mensagem)
        else: # Senão, restando apenas a opção dele estar em um canal de voz:
            await ctx.voice_client.disconnect() #Disconecta o Bot do canal de voz
            
    #Comando para tocar uma música atravez de sua URL.
    @commands.command(name="playurl", help="Toca uma musica através de sua URL, pesquisada no youtube")
    async def playu(self, ctx, url):
            if ctx.author.voice is None:
                await ctx.send("Você não está em um canal")
            elif ctx.voice_client is None:
                voice_channel = ctx.author.voice.channel
                await voice_channel.connect()
            else:
                voice_channel = ctx.author.voice.channel
                await ctx.voice_client.move_to(voice_channel)
            with youtube_dl.YoutubeDL({'default_search': 'auto', 'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                music = await discord.FFmpegOpusAudio.from_probe(url2, method='fallback')
                voice = ctx.voice_client
                voice.play(music)
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
    @commands.command(name="wiki", help="Devolve parte do sumário da wikipédia")
    async def wiki(self, ctx, *text):
        try:
            wikipedia.set_lang("pt")
            wikipedia.summary((' '.join(text)),1)
            pass
        except:
            await ctx.send('Página não encontrada')
            return
        resp = wikipedia.summary((' '.join(text)),3)
        await ctx.send(resp)


def setup(client):
    client.add_cog(comandos(client))
