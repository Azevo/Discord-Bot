import discord
from discord.ext import commands
import youtube_dl
from discord import FFmpegPCMAudio

'''
-----------------ATENÇÂO----------------------
Essa é uma expansão totalmente de meme e não
adiciona nenhuma função útil ao Bot.

Áudios retirados do LuideVerso
Twitter: https://twitter.com/luide
Twitch: http://twitch.tv/luidematos
Youtube: https://www.youtube.com/c/luideverso
-----------------ATENÇÂO----------------------
'''

class comandos(commands.Cog):
    def _init_(self, client):
        self.client = client

    @commands.command(name="djraul", help="TUTURI DANCE")
    async def playu(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        YDL_OPTIONS = {'default_search': 'auto', 'format': 'bestaudio', 'noplaylist':'True'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info('https://www.youtube.com/watch?v=W6HvF9-4HAA', download=False)
            url2 = info['formats'][0]['url']
            music = await discord.FFmpegOpusAudio.from_probe(url2,  method='fallback')
            voice = ctx.voice_client
            await ctx.send("Tocando agora Ehrling - Dance With Me")
            voice.play(music)

    @commands.command(name="corno", help="é o touro chifrudo!")
    async def corno(self, ctx):
        source = FFmpegPCMAudio('TOURO_CHIFRUDO.wav')
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        voice = ctx.voice_client
        voice.play(source)

    @commands.command(name="careca", help="careca desgraçado!")
    async def careca(self, ctx):
        source = FFmpegPCMAudio('CARECA.mp3')
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        voice = ctx.voice_client
        voice.play(source)

    @commands.command(name="policia", help="alo policia federal WOW")
    async def policia(self, ctx):
        source = FFmpegPCMAudio('policia.mp3')
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        voice = ctx.voice_client
        voice.play(source)

    @commands.command(name="rapaz", help="rapaz")
    async def rapaz(self, ctx):
        source = FFmpegPCMAudio('rapaz.mp3')
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        voice = ctx.voice_client
        voice.play(source)
 
    @commands.command(name="momento", help="Momento Histórico para o Brasil!!!")
    async def momento(self, ctx):
        source = FFmpegPCMAudio('hist.mp3')
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal")
        elif ctx.voice_client is None:
            voice_channel = ctx.author.voice.channel
            await voice_channel.connect()
        else:
            voice_channel = ctx.author.voice.channel
            await ctx.voice_client.move_to(voice_channel)
        voice = ctx.voice_client
        voice.play(source)


def setup(client):
    client.add_cog(comandos(client))
