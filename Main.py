import discord
from discord.ext import commands
import asyncio
import time
import os
import bs4, requests
import youtube_dl
from discord import opus

client = commands.Bot(command_prefix = "x")

player = {}

@client.event
async def on_ready():
    print('Logged in as')
    print("User name:", client.user.name)
    print("User id:", client.user.id)
    print('---------------')
    
@client.event
async def on_message(message):
    if message.content == 'xstop':
        serverid = message.server.id
        players[serverid].stop()
    if message.content == 'xpause':
        serverid = message.server.id
        players[serverid].pause()
        await client.send_message(message.channel, "Player paused")
    if message.content == 'xresume':
        serverid = message.server.id
        players[serverid].resume()
        await client.send_message(message.channel, "Player resumed")
    if message.content.startswith('xplay '):
        author = message.author
        name = message.content.replace("xplay ", '')                 
        fullcontent = ('http://www.youtube.com/results?search_query=' + name)
        text = requests.get(fullcontent).text
        soup = bs4.BeautifulSoup(text, 'html.parser')
        img = soup.find_all('img')
        div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
        a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
        title = (a[0]['title'])
        a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
        url = ('http://www.youtube.com'+a0['href'])
        delmsg = await client.send_message(message.channel, 'Now Playing ** >> ' + title + '**')
        server = message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        print("User: {} From Server: {} is playing {}".format(author, server, title))
        player.start()
    await client.process_commands(message)

@client.command(pass_context=True)
async def ping(ctx):
    pingtime = time.time()
    pingms = await client.say("Pinging...")
    ping = (time.time() - pingtime) * 1000
    await client.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
    
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    await client.say('Connected to voice channel: **[' + str(channel) + ']**')
	
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    await client.say('Left voice channel')

client.run(os.environ['BOT_TOKEN'])
