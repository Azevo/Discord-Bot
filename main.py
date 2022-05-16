from discord.ext import commands
import discord
import decouple
client = commands.Bot(command_prefix="!")

client.load_extension('DefsCog')
client.load_extension('MemeCog')
Token = decouple.config("TOKEN")
client.run(Token)
