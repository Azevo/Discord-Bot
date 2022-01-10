import discord
from discord.ext import commands
import youtube_dl
import urllib.request
from Mod import re

class comandos(commands.Cog):
    def _init_(self, client):
        self.client = client
    @commands.command(name="djraul", help="")
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

def setup(client):
    client.add_cog(comandos(client))
