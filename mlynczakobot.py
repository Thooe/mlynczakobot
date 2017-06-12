import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
	print('Logged in as')
	print(bot.user.name)
	print(bot.user.id)
	print(discord.__version__)
	print(discord.AppInfo)
	print('-------')


@bot.command(pass_context=True)
async def ping(ctx):
	await bot.say('Pong!')
	
bot.run('MzIzOTExMTgxMTg0MjcwMzM3.DCCOhg._b1zx0UtYSp6O2BbJNQDmX2-ioc')