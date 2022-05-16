import asyncio
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import urllib.request
import emoji
import youtube_dl
deck_generico_id = ''
audio_data ={':police_officer:' : 'POLICIA',
             ':party_popper:' : 'MOMENTO',
             ':ox:' : 'CORNO',
             ':mouse_face:' : 'RAPAZ',
             ':watch:' : 'CLOCK',
             ':clown_face:' : 'ENGRACADO',
             ':man_bald:' : 'CARECA',
             ':speaking_head:' : 'LACRE',
             ':compass:' : 'PERDIDO',
             ':cowboy_hat_face:' : 'IHA',
             ':old_man:' : 'MENTIRA',
             ':foot:' : 'AI',
             ':red_question_mark:':'PORQUESERA',
             ':rock:':'CRACK',
             ':open_book:':'LIVRINHO',
             ':newspaper:':'NEWS',
             ':judge:':'INJUSTO',
             ':egg:':'OVO',
             ':stop_sign:':'PARE',
             ':no_one_under_eighteen:':'PUTARIA'}
emoji_list = [':police_officer:',':party_popper:',':ox:',':mouse_face:',':watch:',':clown_face:',':man_bald:'
,':speaking_head:',':compass:',':cowboy_hat_face:',':foot:',':red_question_mark:',':rock:',':open_book:',
':newspaper:',':judge:',':egg:',':stop_sign:',':no_one_under_eighteen:']
mensagem_deck01 = '''
----------------------------------Deck de Áudios do Bot----------------------------------

:police_officer: ==> POLICIA // :clown_face: ==> ENGRACADO // :older_man: ==> MENTIRA // :foot: ==> AI
:tada: ==> MOMENTO // :man_bald: ==> CARECA  // :question: ==> SERA // :rock: ==> CRACK
:ox: ==> CORNO // :speaking_head: ==> LACRE // :book: ==> LIVRINHO // :newspaper: ==> NEWS
:mouse: ==> RAPAZ // :compass: ==> PERDIDO // :judge: ==> INJUSTO // :egg: ==> OVINHO
:watch: ==> CLOCK // :cowboy: ==> PROCURA // :stop_sign: ==> PARE // :underage: ==> PUTARIA
----------------------------------------------------------------------------------------------
'''




class Meme(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener('on_ready')
    async def status(self):
        await self.bot.change_presence(activity=discord.Game(name="Tempo fora"))

    @commands.command(name="deck", help='Um total de 20 "efeitos sonoros" para tocar em call')
    async def playu(self,ctx):
        # Inicio padrão para saber se o usuario esta em uma call, e se sim, mover o bot até lá #
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz")
        else:
            if ctx.voice_client is None:
                voice_channel = ctx.author.voice.channel
                await voice_channel.connect()
            else:
                voice_channel = ctx.author.voice.channel
                await ctx.voice_client.move_to(voice_channel)
        # Inicio padrão para saber se o usuario esta em uma call, e se sim, mover o bot até lá #
            menssage = await ctx.send(mensagem_deck01)
            for audio in audio_data:
                await menssage.add_reaction(emoji.emojize(audio))
            deck_generico_id = menssage.id

            def check(reaction,user):
                return user == ctx.author and reaction.message.id == deck_generico_id
            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Deck Fechado')
                    break
                else:
                    audio = str(emoji.demojize(reaction.emoji))
                    print(audio_data.get(audio))
                    source = FFmpegPCMAudio(audio_data.get(audio) + '.mp3')
                    print(emoji.demojize(reaction.emoji))
                    voice = ctx.voice_client
                    try:
                        voice.play(source)
                    except:
                        pass
                    await reaction.remove(user)








def setup(client):
    client.add_cog(Meme(client))
