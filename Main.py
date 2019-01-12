import discord
from discord import commands

bot = commands.Bot(command_prefix = "x")

@bot.event
async def on_ready():
