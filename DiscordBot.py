from discord.ext import commands
import decouple

#Identifica o Robô e qual será o prefixo de comando.
client = commands.Bot(command_prefix="!")
#Carrega o Script Python com os comandos (como o import de uma biblioteca)  
client.load_extension('Defs App')
#Usamos o decouple para tirar de um arquivo .env o Token do Bot
Token = decouple.config("TOKEN")
#Executamos o programa
client.run(Token)
