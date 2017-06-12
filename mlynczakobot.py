import discord
from discord.ext import commands
import random
import os
clear = lambda: os.system('cls')

bot = commands.Bot(command_prefix='!')

list_of_fastfoods = ['kfc','mcdonald','kebab','fastfood','burgerking','wendys']

@bot.event
async def on_ready():
	clear()
	print('Logged in!')
	print('Bot name: '+str(bot.user.name))
	print('Bot id: '+str(bot.user.id))
	print('Api version: '+str(discord.__version__))
	print('---------------------------------')

@bot.event
async def on_message(message):
	if message.content in list_of_fastfoods:
		await bot.add_reaction(message,'🤖')
	await bot.process_commands(message)

@bot.command(pass_context=True)
async def ping(ctx):
	await bot.say('Pong!')

#@bot.command(description='When you joined channel')
#async def howlong():
#	await

@bot.command(pass_context=True,description='When you created your\'s discord account')
async def when(ctx):
	await bot.say("Created at: "+str(ctx.message.author.created_at))

@bot.command(description='Roll number from 0 to 100')
async def roll():
	await bot.say('Rolled:  '+str(random.randint(0,100)))
	
bot.run('MzIzOTExMTgxMTg0MjcwMzM3.DCCOhg._b1zx0UtYSp6O2BbJNQDmX2-ioc')