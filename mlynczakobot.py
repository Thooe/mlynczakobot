from discord.ext import commands
from datetime import datetime
from imdbpie import Imdb
from coinmarketcap import Market

import time
import discord
import random
import ctypes
import sys
import os

import urbandictionary as udic
import xml.etree.ElementTree as ET
tree = ET.parse('tokens.xml')
root = tree.getroot()


def cc(): return os.system('cls')


timer_start = time.time()
bot = commands.Bot(command_prefix='!')

list_of_fastfoods = ['kfc', 'mcdonald', 'kebab', 'fastfood', 'burgerking', 'wendys']

"""get token of certain api"""


def getToken(token):
    for child in root:
        if child.tag == token:
            return child.text
    return


"""on bot start, login"""


@bot.event
async def on_ready():
    cc()
    print('Logged in!\nBot name: {}\nBot id: {}\nApi version: {}\nCreated at: {}'
          .format(bot.user.name, bot.user.id, discord.__version__, bot.user.created_at))
    await bot.change_presence(game=discord.Game(name='fuck reddit', url='Pornhub.com', type=1))
    print('---------------------------------')


"""on incoming message do stuff"""


@bot.event
async def on_message(message):
    m = message.content.lower()
    """react to fastfood restaurants"""
    if m in list_of_fastfoods:
        await bot.add_reaction(message, '🤖')
    """react to fuck you message"""
    if m == 'fuck you':
        await bot.add_reaction(message, '🔫')
        await bot.send_message(message.channel, 'fuck you too')
    """fuck supreme"""
    if 'supreme' in m:
        if not message.author.bot:
            await bot.send_message(message.channel, 'fuck supreme❗')
    await bot.process_commands(message)

"""when someone join server do stuff"""


@bot.event
async def on_member_join(member):
    await bot.send_message(member.server, 'Witaj {} ! 😍'.format(member.name))
    role = discord.utils.get(member.server.roles, name='Plebs')
    await bot.add_roles(member, role)

"""On error do stuff"""


@bot.event
async def on_command_error(error, ctx):
    print(error, ctx)
    if isinstance(error, commands.BadArgument):
        if ctx.command.qualified_name == 'user':
            await bot.send_message(ctx.message.channel, '⚠ Użytkownik nie znajduje się na tym serwerze! ⚠')
    elif isinstance(error, commands.CommandNotFound):
        await bot.send_message(ctx.message.channel, '{} ⚠ Nie ma takiej komendy! ⚠'.format(ctx.message.author.mention))
    return bot

"""
channel info
"""

"""print user info"""


@bot.command(pass_context=True)
async def user(ctx, *, m: discord.Member=None):
    if not m:
        m = ctx.message.author

    avatar = m.avatar_url
    if m.avatar_url == '':
        avatar = m.default_avatar_url

    game = m.game
    if not m.game:
        game = 'Nie gra'

    member_number = sorted(ctx.message.server.members, key=lambda u: u.joined_at).index(m) + 1

    roles = ''
    roles_count = 0
    for r in m.roles:
        if r.name != '@everyone':
            roles_count = roles_count + 1
            roles = roles + '{}, '.format(r.name)
    roles = roles[:-2]

    em = discord.Embed(colour=0x2F4F4F)
    (em
     .add_field(name='Nazwa:', value=m, inline=True)
     .add_field(name='Status:', value=str(m.status).capitalize(), inline=True)
     .add_field(name='Gra:', value=game, inline=True)
     .add_field(name='ID:', value=m.id, inline=True)
     .add_field(name='Dołączył na pozycji:', value=member_number, inline=True)
     .add_field(name='Dołączył:', value=datetime.strptime(str(m.joined_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'), inline=True)
     .add_field(name='Utworzony :', value=datetime.strptime(str(m.created_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S'), inline=True)
     .add_field(name='({}) Roles:'.format(roles_count), value=roles, inline=True)
     .set_thumbnail(url=avatar))
    await bot.send_message(ctx.message.channel, embed=em)

"""print server info"""


@bot.command(pass_context=True)
async def server(ctx):
    s = ctx.message.server
    em = discord.Embed(colour=0x2F4F4F)
    text_channels = 0
    voice_channels = 0
    how_many_roles = 0
    online_users = 0
    emojis = ''
    for e in s.emojis:
        emojis = emojis + ' ' + str(e)
    for m in s.members:
        if m.status != m.status.offline:
            online_users = online_users + 1
    for r in s.roles:
        how_many_roles = how_many_roles + 1
    for ch in s.channels:
        if ch.type == discord.ChannelType.text:
            text_channels = text_channels + 1
        if ch.type == discord.ChannelType.voice:
            voice_channels = voice_channels + 1
    ver = s.verification_level
    if ver == discord.VerificationLevel.none:
        ver = 'Brak'
    utc = datetime.strptime(str(s.created_at.replace(microsecond=0)), '%Y-%m-%d %H:%M:%S')
    (em
     .set_footer(text='Informacje o serwerze', icon_url=bot.user.avatar_url)
     .add_field(name='Nazwa Servera:', value=s.name, inline=True)
     .add_field(name='Właściciel:', value=s.owner, inline=True)
     .add_field(name='Server ID:', value=s.id, inline=True)
     .add_field(name='Stworzony:', value=utc, inline=True)
     .add_field(name='Region:', value=s.region, inline=True)
     .add_field(name='Ról:', value=how_many_roles, inline=True)
     .add_field(name='Kanałów głosowych:', value=voice_channels, inline=True)
     .add_field(name='Kanałów textowych:', value=text_channels, inline=True)
     .add_field(name='Poziom weryfikacji:', value=ver, inline=True)
     .add_field(name='Online:', value='{}/{}'.format(online_users, s.member_count), inline=True)
     .add_field(name='Emoji:', value=emojis, inline=True)
     .set_thumbnail(url=s.icon_url))
    await bot.send_message(ctx.message.channel, embed=em)

"""clear messeges"""


@bot.command(pass_context=True)
async def clear(ctx, amount: int = 10):
    await bot.purge_from(ctx.message.channel, limit=amount)

"""stock"""


@bot.command(pass_context=True)
async def stock(currency: str=None):
    await bot.say(ctx.message.channel, '')


"""imdb"""

idb = Imdb()


@bot.command(pass_context=True)
async def imdb(ctx, *, image: str=None):
    if not image:
        await bot.send_message(ctx.message.channel,
                               '{} ⚠ You need to specify name of movie or tv show! ⚠\n\n Example: !imdb La La Land'
                               .format(ctx.message.author.mention))
    else:
        data = idb.search_for_title(''.join(image))
        if not data:
            await bot.send_message(ctx.message.channel,
                                   '{} ⚠ Not found! ⚠'.format(ctx.message.author.mention))
        else:
            i = idb.get_title_by_id(data[0].get('imdb_id'))

            i_genres = i.genres
            genres = ''
            if i_genres:
                for g in i_genres:
                    genres = genres + g + ', '
                genres = genres[:-2]
            else:
                genres = None

            s = i.runtime
            em = discord.Embed(colour=0xFFD219, title=i.title, description=i.plot_outline,
                               url='http://imdb.com/title/{}/'.format(i.imdb_id))

            i_type = i.type
            if i_type == 'feature':
                if i.directors_summary:
                    name = 'Directors:'
                    directors = ''
                    directors_count = 0
                    for d in i.directors_summary:
                        directors = directors + d.name + ', '
                        directors_count = directors_count + 1
                        directors = directors[:-2]
                    if directors_count < 2:
                        name = name.replace('s', '')
                    i_type = 'Movie'
                    em.add_field(name=name, value=directors, inline=True)

            elif i_type == 'tv_series':
                i_type = 'TV series'
                episodes = idb.get_episodes(i.imdb_id)
                count_episodes = len(episodes)
                if count_episodes:
                    em.add_field(name='Episodes:', value=count_episodes, inline=True)
            elif i_type == 'short':
                i_type = 'Short'
            else:
                print('Type to involve in code: {}'.format(i_type))

            s_str = ''
            if s:
                s_str = '{:02}h {:02}min'.format(s // 3600, s % 3600 // 60)
            else:
                s_str = '0s'
            cover_url = i.cover_url
            if cover_url:
                em.set_thumbnail(url=i.cover_url)
            (em
             .add_field(name='Type:', value=i_type, inline=True)
             .add_field(name='Genres:', value=genres, inline=True)
             .add_field(name='Year:', value=i.year, inline=True)
             .add_field(name='Rating:', value='{}/10'.format(i.rating), inline=True)
             .add_field(name='Certification:', value=i.certification, inline=True)
             .add_field(name='Runtime:', value=s_str, inline=True)
             .set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url))

            await bot.send_message(ctx.message.channel, embed=em)

""""imdb popular shows"""


@bot.command(pass_context=True)
async def imdbpopular(ctx):

    _popular_shows = idb.popular_shows()
    _popular_shows = _popular_shows[:-40]

    em = discord.Embed(colour=0xFFD219)

    top10 = ''
    for i, e in enumerate(_popular_shows):
        top10 = top10 + '{}. {}\n\n'.format(i + 1, e.get('title'))

    em.add_field(name='Top 10 most popular shows on imdb:\n',
                 value=top10)

    await bot.send_message(ctx.message.channel, embed=em)

"""random urban dictionary"""


@bot.command(pass_context=True)
async def rud(ctx):
    await udi(ctx, random=True)

"""urban dictionary"""


@bot.command(pass_context=True)
async def ud(ctx, *, words: str=None):
    await udi(ctx, words)

"""urban dictionary"""


async def udi(ctx, words=None, random=False):
    em = discord.Embed(colour=0x2F4F4F)
    (em
     .set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url)
     .set_thumbnail(url=bot.user.avatar_url))

    defs = []
    if not random:
        if not words:
            await bot.send_message(ctx.message.channel, '{} ⚠ Nie podałeś słowa ⚠'.format(ctx.message.author.mention))
        else:
            defs = udic.define(words)
    else:
        defs = udic.random()

    if len(defs):
        em.add_field(name=defs[0].word, value=defs[0].definition, inline=True)
        await bot.send_message(ctx.message.channel, embed=em)
    else:
        if words:
            await bot.send_message(ctx.message.channel, '{} ⚠ Nie znaleziono słowa ⚠'.format(ctx.message.author.mention))


def getdlist(data, arg, index=0):
    return data[index].get(arg)


"""Cryptocurrency Info"""

coinmarketcap = Market()


@bot.command(pass_context=True)
async def crypto(ctx, currency, convert='USD'):
    data = []
    try:
        data = coinmarketcap.ticker(currency, convert=convert)
    except:
        await bot.send_message(ctx.message.channel,
                               '⚠{} Currency {} was not found!⚠'.format(ctx.message.author.mention, currency))
        return

    em = discord.Embed(colour=0xFFD219, title=getdlist(data, 'name'),
                       url='https://coinmarketcap.com/currencies/{}/'.format(getdlist(data, 'id')))

    last_updated = time.ctime(int(getdlist(data, 'last_updated')))
    price = getdlist(data, 'price_usd')

    if convert != 'USD':
        price = getdlist(data, 'price_{}'.format(convert.lower()))

    if not price:
        await bot.send_message(ctx.message.channel,
                               '⚠{} Currency convert type {} was not found!⚠'.format(ctx.message.author.mention, convert))
        return

    (em
     .add_field(name='ID:', value=getdlist(data, 'id'), inline=True)
     .add_field(name='Symbol:', value=getdlist(data, 'symbol'), inline=True)
     .add_field(name='Rank:', value=getdlist(data, 'rank'), inline=True)
     .add_field(name='Price:', value='{} {}'.format(price, convert.upper()), inline=True)
     .add_field(name='BTC Price:', value=getdlist(data, 'price_btc') + ' BTC', inline=True)
     .add_field(name='Change 1h:', value=getdlist(data, 'percent_change_1h') + ' \%', inline=True)
     .add_field(name='Change 24h:', value=getdlist(data, 'percent_change_24h') + ' \%', inline=True)
     .add_field(name='Change 7d:', value=getdlist(data, 'percent_change_7d') + ' \%', inline=True)
     .add_field(name='Last updated:', value=last_updated, inline=True)
     .set_footer(text=ctx.message.author, icon_url=ctx.message.author.avatar_url))

    await bot.send_message(ctx.message.channel, embed=em)

"""Cryptocurrency Top list info"""


@bot.command(pass_context=True)
async def cryptotop(ctx, convert='USD'):
    data = coinmarketcap.ticker(limit=10, convert='EUR')

    top10 = ''
    for i, e in enumerate(data):
        top10 = top10 + '{}. {}\n\n'.format(i + 1, e.get('name'))

    em = discord.Embed(colour=0xFFD219, title='Top 10 Crypto currencies.',
                       url='https://coinmarketcap.com/', description=top10)

    await bot.send_message(ctx.message.channel, embed=em)

"""Bot uptime"""


@bot.command(pass_context=True)
async def uptime(ctx):
    uptime = time.time() - timer_start
    t = int(uptime)
    await bot.say('{:02}h {:02}m {:02}s'.format(t // 3600, t % 3600 // 60, t % 60))

"""russian roulette"""


@bot.command(pass_context=True)
async def rrol(ctx):
    await bot.add_reaction(ctx.message, '😱')
    if random.randint(1, 6) == 1:
        await bot.say(ctx.message.author.mention + ' 💀🔫')
        await bot.ban(ctx.message.author, delete_message_days=0)
    else:
        await bot.say('{} 🍀 to twój szczęśliwy dzień! 🍀'.format(ctx.message.author.mention))

"""roll number from 0 to 100"""


@bot.command()
async def roll(number: int=100):
    await bot.say('🎲 Wylosowano: {}'.format(random.randint(0, number)))

"""echo"""


@bot.command()
async def echo(*, word):
    await bot.say(word)

bot.run(getToken('Discord'))
