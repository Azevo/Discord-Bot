from discord.ext import commands
import discord
import decouple
import youtube_dl
import urllib.request
from Mod import re
client = commands.Bot(command_prefix="!")


@client.command(name="toca", help="Toca uma musica através de seu título ou URL do youtube")
async def tocar(ctx, *text):
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
    if 'https' in str(text):
        texto = (' '.join(text))
        url = texto
        pass
    else:
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
                for titulo in titulos:
                    await ctx.send('{:2} {}'.format((titulos.index(titulo)+1), titulo))
                await ctx.send("Escolha entre 1, 2, 3, 4 ou 5")
                try:
                    msg = await client.wait_for("message", check=check, timeout=60)
                    m = msg.content.lower()
                except:
                    await ctx.send("Vai responder ?")
                await ctx.send("Você escolheu "+ str(m))
                musica = titulos.pop((int(m)-1))
                musica2 = video_ids.pop((int(m)-1))
                url = 'https://www.youtube.com/watch?v='+ musica2
                break
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max ','options': '-vn'}
    with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'noplaylist':'True' , 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        music = await discord.FFmpegOpusAudio.from_probe(url2, **{'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'})
        discord.utils.get(client.voice_clients, guild=ctx.guild).play(music)


client.load_extension('defs_app')
client.load_extension('meme_app')

Token = decouple.config("TOKEN")
client.run(Token)
