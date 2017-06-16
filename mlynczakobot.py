from discord.ext import commands
from datetime import datetime

import discord
import random
import ctypes, sys
import os

import xml.etree.ElementTree as ET
tree = ET.parse('tokens.xml')
root = tree.getroot()
clear = lambda: os.system('cls')

bot = commands.Bot(command_prefix='!')

list_of_fastfoods = ['kfc','mcdonald','kebab','fastfood','burgerking','wendys']

"""get token of certain api"""
def getToken(token):
	for child in root:
		if child.tag == token:
			return child.text
	return

"""on bot start, login"""
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

"""on incoming message do stuff"""
@bot.event
async def on_message(message):
	"""react to fastfood restaurants"""
	if message.content in list_of_fastfoods:
		await bot.add_reaction(message,'🤖')
	"""react to fuck you message"""
	if message.content == 'fuck you':
		await bot.add_reaction(message,'🔫')
		await bot.send_message(message.channel, 'fuck you too')
	await bot.process_commands(message)

"""when someone join server do stuff"""
@bot.event
async def on_member_join(member):
	await bot.send_message(member.server, 'Witaj '+member.name+' ! 😍')
	role = discord.utils.get(member.server.roles, name='Plebs')
	await bot.add_roles(member, role)

"""On error do stuff"""
@bot.event
async def on_command_error(error, ctx):
	print(error,ctx)
	if isinstance(error, commands.BadArgument):
		if ctx.command.qualified_name == 'userinfo':
			await bot.send_message(ctx.message.channel, '⚠ Użytkownik nie znajduje się na tym serwerze! ⚠')

"""
channel info
"""

"""print user info"""
@bot.command(pass_context=True)
async def user(ctx, *, m : discord.Member=None):
	if not m:
			m = ctx.message.author

	avatar = m.avatar_url
	if m.avatar_url == '':
		avatar = m.default_avatar_url

	game = m.game
	if not m.game:
		game = 'Nie gra'

	member_number = sorted(ctx.message.server.members, key=lambda u: u.joined_at).index(m) + 1

	roles=''
	roles_count = 0
	for r in m.roles:
		if r.name != '@everyone':
			roles_count = roles_count +1
			roles = roles + '{}, '.format(r.name)
	roles = roles[:-2]

	si = discord.Embed(colour=0x2F4F4F)
	(si
	.add_field(name='Nazwa:',value=m, inline=True)
	.add_field(name='Status:',value=str(m.status).capitalize(), inline=True)
	.add_field(name='Gra:',value=game, inline=True)
	.add_field(name='ID:',value=m.id, inline=True)
	.add_field(name='Dołączył na pozycji:',value=member_number, inline=True)
	.add_field(name='Dołączył:',value=datetime.strptime(str(m.joined_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'), inline=True)
	.add_field(name='Utworzony :',value=datetime.strptime(str(m.created_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'), inline=True)
	.add_field(name='({}) Roles:'.format(roles_count),value=roles, inline=True)
	.set_thumbnail(url=avatar))
	await bot.send_message(ctx.message.channel, embed=si)

"""print server info"""
@bot.command(pass_context=True)
async def server(ctx):
	s = ctx.message.server
	si = discord.Embed(colour=0x2F4F4F)
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
	ver = s.verification_level
	if ver == discord.VerificationLevel.none:
		ver = 'Brak'
	utc = datetime.strptime(str(s.created_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
	(si
	.set_footer(text='Informacje o serwerze', icon_url=bot.user.avatar_url)
	.add_field(name='Nazwa Servera:',value=s.name, inline=True)
	.add_field(name='Właściciel:',value=s.owner, inline=True)
	.add_field(name='Server ID:',value=s.id, inline=True)
	.add_field(name='Stworzony:',value=utc, inline=True)
	.add_field(name='Region:',value=s.region, inline=True)
	.add_field(name='Ról:',value=how_many_roles, inline=True)
	.add_field(name='Kanałów głosowych:',value=voice_channels, inline=True)
	.add_field(name='Kanałów textowych:',value=text_channels, inline=True)
	.add_field(name='Poziom weryfikacji:',value=ver, inline=True)
	.add_field(name='Online:',value=str(online_users)+'/'+str(s.member_count), inline=True)
	.add_field(name='Emoji:',value=emojis, inline=True)
	.set_thumbnail(url=s.icon_url))
	await bot.send_message(ctx.message.channel, embed=si)

"""stock"""
@bot.command(pass_context=True)
async def stock(currency : str = None):
	await bot.say('')

"""russian roulette"""
@bot.command(pass_context=True)
async def rrol(ctx):
	await bot.add_reaction(ctx.message,'😱')
	r = random.randint(1,6)
	if r == 1:
		await bot.say(ctx.message.author.mention+' 💀🔫')
		await bot.ban(ctx.message.author, delete_message_days=0)
	else:
		await bot.say('🍀 '+ctx.message.author.mention+' to twój szczęśliwy dzień! 🍀')

"""roll number from 0 to 100"""
@bot.command()
async def roll(number : int = None):
	if number == None:
		number = 100
	await bot.say('🎲 Wylosowano:  '+str(random.randint(0,number)))

bot.run(getToken('Discord'))
