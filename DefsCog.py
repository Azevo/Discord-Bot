import random
import discord
import asyncio
from discord.ext import commands
import youtube_dl
import pytube
from pytube import YouTube
import emoji

'''

----------------------------- Atualização do dia 15/04/2022 ------------------------------------------

Sistema pouco pensado (e com muito a melhorar) de playlist e autoplay, mas funciona.

------------------------------------------------------------------------------------------------------

Leia-se usuário como aquele que manda uma mensagem com o prefixo "!" em algum canal de mensagem, onde:
* O usuário é o author da mensagem.
* A mensagem é o comando + texto. 
* O canal de voz ou mensagem é o ctx (contexto).
* O cliente é o Bot.

------------------------------------------------------------------------------------------------------
'''

sorteio_frases = ['Eu escolhi ','Acho que é melhor ','Hoje eu vou de ','Vou de ','Acho que ','Prefiro ']
opcoes_emojis = {':keycap_1:':'1',
':keycap_2:':'2',
':keycap_3:':'3',
':keycap_4:':'4',
':keycap_5:':'5'}
num_music = 0
interpretar_emojis = {':last_track_button:':'volte',':stop_button:': 'vaze' ,':play_or_pause_button:':'pare',':next_track_button:':'avance'}
FFMPEG_OPTIONS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
mensagem_painel = '''
--------Painel de Música-------

 Volta    Vaza    Pausa   Avança
-----------------------------------
'''




class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_listener(self.on_reaction_add,"on_reaction_add")
        self.states = {}
        self.pos_url = []
        self.pass_url = []
        self.atual_url = ''

    @commands.command(name="toca",aliases=['tocar','p','t'], help="Toca uma musica através de seu título, pesquisado no youtube")
    async def tocar(self, ctx, *text):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz")
            raise commands.CommandError("Você não está em um canal de voz")
        else:
            if ctx.voice_client is None:
                voice_channel = ctx.author.voice.channel
                await voice_channel.connect()
                pass
            else:
                voice_channel = ctx.author.voice.channel
                await ctx.voice_client.move_to(voice_channel)
                pass

            titulos = []
            video_urls = []
            musica = self.bot.get_cog('Music')
            if 'https://youtu' and 'list=' in str(text):
                texto = (' '.join(text))
                url = texto
                await musica.painel(ctx)
                await musica.play(ctx,url,playlist=True)
            elif 'https://youtu' in str(text):
                texto = (' '.join(text))
                url = texto
                await musica.painel(ctx)
                await musica.play(ctx,url,playlist=False)
            else:
                search_keyword = (' '.join(text))
                pesquisa = pytube.Search(search_keyword)
                resultados = pesquisa.results
                for video in resultados:
                    video_url = video.watch_url
                    video_urls.append(video_url)
                    titulo = video.title
                    titulos.append(titulo)
                    mensagem = []
                    if len(titulos) == 5:
                        mensagem.append("Títulos encontrados: {}".format('\n'))
                        for titulo in titulos:
                            mensagem.append('{:2}  {:2} {}'.format((titulos.index(titulo)+1), titulo, '\n'))
                        mensagem.append("Escolha entre 1, 2, 3, 4 ou 5")
                        mensagem = ' '.join(mensagem)
                        menssagem = await ctx.send(mensagem)
                        for emojo in opcoes_emojis:
                            await menssagem.add_reaction(emoji.emojize(emojo))
                        deck_id = menssagem.id

                        def check(reaction,user):
                            return user == ctx.author and emoji.demojize(reaction.emoji) in opcoes_emojis and reaction.message.id == deck_id
                        try:
                            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                            m = int(opcoes_emojis.get(emoji.demojize(reaction.emoji)))
                        except asyncio.TimeoutError:
                            await ctx.send("Resposta não recebida, comando expirado")
                        else:
                            #await ctx.send("Você escolheu "+ str(m))
                            musica_titulo = titulos.pop((int(m)-1))
                            musica2 = video_urls.pop((int(m)-1))
                            url =  musica2
                            await ctx.send("Você escolheu "+ url)
                            await reaction.remove(user)
                            await musica.painel(ctx)
                            await musica.play(ctx,url,playlist=False)
                            break


    @commands.command(name="play", hidden=True)
    async def play(self, ctx, url, playlist : bool):
        musica = self.bot.get_cog('Music')
        pos_url = self.pos_url
        pass_url = self.pass_url
        atual_url = self.atual_url
        if playlist==False:
            print(ctx)
            print(url)
            print(playlist)
            voice = ctx.voice_client

            def pos_musica(a):
                if len(pos_url)== 0:
                    pass
                else:
                    url = pos_url.pop(0)
                    if len(pass_url) >= 2:
                        atual_url = pass_url.pop(0)
                        pass_url.append(url)
                    else:
                        pass_url.append(url)
                    print(pass_url)
                    with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'noplaylist':'True' , 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}) as ydl:
                        info = ydl.extract_info(url, download=False)
                        url2 = info['formats'][0]['url']
                        music = discord.FFmpegOpusAudio(url2, before_options=FFMPEG_OPTIONS)
                        voice.play(music,after=pos_musica)

            if voice.is_playing():
                await musica.lista_reproducao(ctx,url,modo=True,playlist=False)
            
            else:
                with youtube_dl.YoutubeDL({'format': 'bestaudio/best', 'noplaylist':'True' , 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    await musica.listar_passada(ctx,url,modo=True)
                    music = discord.FFmpegOpusAudio(url2, before_options=FFMPEG_OPTIONS)
                    voice.play(music,after=pos_musica)

        elif playlist==True:
            await musica.lista_reproducao(ctx,url,modo=True,playlist=True)
            
    async def lista_reproducao(self,ctx,url,modo:bool,playlist:bool):
        music = self.bot.get_cog('Music')
        num_music = 0
        pos_url = self.pos_url
        print('modo= '+ str(modo))
        if modo==True and len(pos_url) <= 100 and playlist==False:
            pos_url.append(url)
            video = YouTube(url)
            print(pos_url)
            await ctx.send('{} foi adicionado a lista'.format(video.title))
        elif modo==True and len(pos_url) <= 100 and playlist==True:
            pos_url.clear()
            playlist = pytube.Playlist(url)
            for url in playlist.video_urls:
                try:
                    pos_url.append(url)
                    num_music = num_music + 1
                except:
                    pass
            print(pos_url)
            await ctx.send('{} videos adicionados a lista'.format(num_music))
            url = pos_url.pop(0)
            await music.play(ctx,url,playlist=False)
        elif modo==False:
            if len(pos_url)== 0:
                await ctx.send('Não ha mais itens na lista')
            else:
                #await ctx.send(pos_url)
                url = pos_url.pop(0)
                await music.play(ctx,url,playlist=False)
        else:
            if len(pos_url) > 100:
                ctx.send('lista de reprodução cheia: {}/100'.format(len(pos_url)))


    async def listar_passada(self,ctx,url,modo:bool):
        music = self.bot.get_cog('Music')
        pass_url = self.pass_url
        pos_url = self.pos_url
        voice = ctx.voice_client
        if modo==True:
            if len(pass_url) >= 2:
                lix = pass_url.pop(0)
                pass_url.append(url)
            else:
                pass_url.append(url)
        elif modo==False:
            if len(pass_url)== 0:
                await ctx.send('Sem musica anterior')
            elif len(pass_url) > 0:
                url = pass_url.pop(0)
                pos_url.insert(0,url)
                if len(pass_url) >= 1:
                    purl = pass_url.pop(0)
                    pos_url.insert(1,purl)
            voice.stop()
                
    @commands.command(name="painel", help="Painel de comandos da música")
    async def painel(self,ctx):
        menssagem = await ctx.send(mensagem_painel)
        for emojo in interpretar_emojis:
            await menssagem.add_reaction(emoji.emojize(emojo))

    async def on_reaction_add(self, reaction, user):
        pass_url = self.pass_url
        message = reaction.message
        pass_url = self.pass_url
        pos_url = self.pos_url
        music = self.bot.get_cog('Music')
        ctx = await self.bot.get_context(message)
        voice = ctx.voice_client


        async def tirar(ctx):
            if voice is None:
                await ctx.send("O Bot não está em um canal")
            else:
                pass_url.clear()
                pos_url.clear()
                await voice.disconnect()

        async def pausar(ctx):
            if voice is None:
                await ctx.send("Não tem oque parar")
            else:
                if voice.is_playing():
                    voice.pause()
                elif voice.is_paused():
                    voice.resume()

        async def avancar(ctx):
            if len(pos_url)== 0:
                await ctx.send('Não ha mais itens na lista')
            else:
                voice.stop()

        async def voltar(ctx):
            if len(pass_url)== 0:
                await ctx.send('Sem musica anterior')
            else:
                await music.listar_passada(ctx,url=None,modo=False)
        
        if user != self.bot.user and message.author == self.bot.user:
            comando = str(interpretar_emojis.get(emoji.demojize(reaction.emoji)))
            await reaction.remove(user)
            if comando == 'volte':
                await voltar(ctx)
            elif comando == 'vaze':
                await tirar(ctx)
            elif comando == 'pare':
                await pausar(ctx)
            elif comando == 'avance':
                await avancar(ctx)
            else:
                pass


class Outros(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sorteio", help="Sorteia uma das opções, separadas por '/'")
    async def sort(self, ctx, *text):
        text =  (' '.join(text))
        text = text.split('/')
        opticoes = list(text)
        escolha = random.choice(opticoes)
        await ctx.send(str(random.choice(sorteio_frases)) + str(escolha))


def setup(client):
    client.add_cog(Music(client))
    client.add_cog(Outros(client))
