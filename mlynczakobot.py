import discord
from discord.ext import commands
import random
import ctypes, sys
import os
import xml.etree.ElementTree as ET
tree = ET.parse('tokens.xml')
root = tree.getroot()
clear = lambda: os.system('cls')

bot = commands.Bot(command_prefix='!')

list_of_fastfoods = ['kfc','mcdonald','kebab','fastfood','burgerking','wendys']

#get token of certain api
def getToken(token):
	for child in root:
		if child.tag == token:
			return child.text
	return

#on bot start, login
@bot.event
async def on_ready():
	clear()
	print('Logged in!')
	print('Bot name: '+str(bot.user.name))
	print('Bot id: '+str(bot.user.id))
	print('Api version: '+str(discord.__version__))
	print('Created at: '+str(bot.user.created_at))
	#await bot.change_status(discord.Game(name='fuck reddit',type=1))
	await bot.change_presence(game=discord.Game(name='fuck reddit'))
	print('---------------------------------')
	
#react to fastfood restaurants
@bot.event
async def on_message(message):
	if message.content in list_of_fastfoods:
		await bot.add_reaction(message,'🤖')
	await bot.process_commands(message)
	
#react to fuck you message
@bot.event
async def on_message(message):
	if message.content == 'fuck you':
		await bot.add_reaction(message,'🔫')
		await bot.send_message(message.channel, 'fuck you too')
	await bot.process_commands(message)

#when user created discord account
@bot.command(pass_context=True,description='When you created your\'s discord account')
async def when(ctx):
	await bot.say("Created at: "+str(ctx.message.author.created_at))

#roll number from 0 to 100
@bot.command(description='Roll number from 0 to 100')
async def roll():
	await bot.say('Rolled:  '+str(random.randint(0,100)))

bot.run(getToken('Discord'))