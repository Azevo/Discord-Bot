import discord
from discord.ext import commands
import youtube_dl
import urllib.request
from Mod import re
import wikipedia

'''

----------------------------- Atualização do dia 04/02/2022 ------------------------------------------

Por conta de eu  ter baixado a parte a biblioteca re.
O "from Mod import re" foi necessário na minha maquina.
Mas na teoria a biblioteca faz parte da versão padrão do Python.
E só precisaria escrever "import re".

------------------------------------------------------------------------------------------------------

Leia-se usuário como aquele que manda uma mensagem com o prefixo "!" em algum canal de mensagem, onde:
* O usuário é o author da mensagem.
* A mensagem é o comando + texto. 
* O canal de voz ou mensagem é o ctx (contexto).
* O cliente é o Bot.

------------------------------------------------------------------------------------------------------
'''

class comandos(commands.Cog):
    def _init_(self, client):
        self.client = client

    @commands.command(name="tira", help="Retira da música que estiver tocando")
    async def tirar(self, ctx):
        voice = ctx.voice_client #Define 'voice' como o canal de voz conectado do Bot
        voice.stop() #Retira o áudio
        await ctx.send("Música retirada") #Avisa que a música foi retirada

    @commands.command(name="pare", help="Para a música que estiver tocando")
    async def parar(self, ctx):
        voice = ctx.voice_client #Define 'voice' como o canal de voz conectado do Bot
        if voice.is_playing(): #Se o Bot estiver reproduzindo áudio ele pausa e avisa que parou
            voice.pause()
            await ctx.send("Tô parado")
        else: #Caso contrário envia, no contexto em que foi chamado, um aviso que o Bot não tem oque pausar
            await ctx.send("Não tem oque parar")

    @commands.command(name="continue", help="Continua a música parada")
    async def resume(self, ctx):
        voice = ctx.voice_client #Define 'voice' como o canal de voz conectado do Bot
        if voice.is_paused(): #Se o Bot estiver pausado ele volta a reproduzir áudio
            voice.resume()
        else: #Caso contrário envia, no contexto em que foi chamado, um aviso que o Bot não está pausado
            await ctx.send("Mas não tá parado")

    @commands.command(name="wiki", help="Devolve parte do sumário da wikipédia")
    async def wiki(self, ctx, *text):
        try:
            wikipedia.set_lang("pt") #Configura a busca para a wikipédia em português
            wikipedia.summary((' '.join(text)),1) #Tenta buscar uma página relativa ao 'text'
            pass
        except: #Caso não consiga ou não encontre a página
            await ctx.send('Página não encontrada') #Envia uma mensagem avisando do erro
            return
        resp = wikipedia.summary((' '.join(text)),3) #Guarda em 'resp' a introdução 
        await ctx.send(resp) #Envia a parte do sumário


def setup(client):
    client.add_cog(comandos(client))
