import discord
from discord.ext import commands
import random
import ctypes, sys
import os
from datetime import datetime
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
	await bot.change_presence(game=discord.Game(name='fuck reddit',url = 'Pornhub.com',type=1))
	print('---------------------------------')

#on incoming message do stuff
@bot.event
async def on_message(message):
	#react to fastfood restaurants
	if message.content in list_of_fastfoods:
		await bot.add_reaction(message,'🤖')
	#react to fuck you message
	if message.content == 'fuck you':
		await bot.add_reaction(message,'🔫')
		await bot.send_message(message.channel, 'fuck you too')
	await bot.process_commands(message)

#when someone join server do stuff
@bot.event
async def on_member_join(member):
	await bot.send_message(member.server, 'Witaj '+member.name+' ! 😍')
	role = discord.utils.get(member.server.roles, name='Plebs')
	await bot.add_roles(member, role)

#when user created discord account
@bot.command(pass_context=True,description='When you created your\'s discord account')
async def kiedy(ctx):
	await bot.say('Twoje konto zostało utworzone: '+str(ctx.message.author.created_at))

#print server info
@bot.command(pass_context=True)
async def serverinfo(ctx):
	s = ctx.message.server
	si = discord.Embed(colour=0x2F4F4F)
	created_at = s.created_at
	text_channels = 0
	voice_channels = 0
	how_many_roles = 0
	online_users = 0
	emojis = ''
	for e in s.emojis:
		emojis = emojis +' '+str(e)
	for m in s.members:
		if m.status != m.status.offline:
			online_users = online_users +1
	for r in s.roles:
		how_many_roles = how_many_roles +1
	for ch in s.channels:
		if ch.type == discord.ChannelType.text:
			text_channels = text_channels +1
		if ch.type == discord.ChannelType.voice:
			voice_channels = voice_channels +1

	utc = datetime.strptime(str(created_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
	(si
	.set_footer(text='Informacje o serwerze', icon_url=bot.user.avatar_url)
	.add_field(name='Nazwa Servera:',value=s.name, inline=True)
	.add_field(name='Właściciel:',value=s.owner.mention, inline=True)
	.add_field(name='Server ID:',value=s.id, inline=True)
	.add_field(name='Stworzony:',value=utc, inline=True)
	.add_field(name='Region:',value=s.region, inline=True)
	.add_field(name='Roles:',value=how_many_roles, inline=True)
	.add_field(name='Kanałów głosowych:',value=voice_channels, inline=True)
	.add_field(name='Kanałów textowych:',value=text_channels, inline=True)
	.add_field(name='Poziom weryfikacji:',value=s.verification_level, inline=True)
	.add_field(name='Online:',value=str(online_users)+'/'+str(s.member_count), inline=True)
	.add_field(name='Emoji:',value=emojis, inline=True)
	.set_thumbnail(url=s.icon_url))
	await bot.send_message(ctx.message.channel, embed=si)

#russian roulette
@bot.command(pass_context=True)
async def rrol(ctx):
	await bot.add_reaction(ctx.message,'😱')
	r = random.randint(1,6)
	if r == 1:
		await bot.say(ctx.message.author.mention+' 💀🔫')
		await bot.ban(ctx.message.author, delete_message_days=0)
	else:
		await bot.say('🍀 '+ctx.message.author.mention+' to twój szczęśliwy dzień! 🍀')

#roll number from 0 to 100
@bot.command(description='Roll number from 0 to 100')
async def roll():
	await bot.say('🎲 Wylosowano:  '+str(random.randint(0,100)))

bot.run(getToken('Discord'))
