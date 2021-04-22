import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import random

######################################################EDIT YOUR BOT HERE##################################################################################################

token = '' #enter bot token here

bot = commands.Bot(command_prefix='!') #you can change the command prefix here

############################################################################################################################################################################


@bot.event
async def on_ready():
    print('hunting horn go brrrrrr')

queue = []
current_playing = None
is_playing = False
buffs = ['ail', 'atk', 'def', 'divine', 'ear', 'hp', 'rec', 'stam', 'stun', 'ele']

ytdl_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' 
}

ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def search(query):

    with YoutubeDL(ytdl_options) as ydl:
        
        info = ydl.extract_info(f'ytsearch:{query}', download=False)['entries'][0]

    return {'link': info['formats'][0]['url'], 'title': info['title']}

def play_next(vc):

    global queue
    global is_playing
    global current_playing

    if len(queue) > 0:
        is_playing = True

        video_link = queue[0]['link']
        current_playing = queue[0]
        queue.pop(0)

        vc.play(FFmpegPCMAudio(video_link, **ffmpeg_options), after=lambda e: play_next(vc))
    else:
        is_playing = False

async def play_music(vc):

    global queue
    global is_playing
    global current_playing

    if len(queue) > 0:
        is_playing = True

        video_link = queue[0]['link']
        current_playing = queue[0]
        queue.pop(0)

        vc.play(FFmpegPCMAudio(video_link, **ffmpeg_options), after=lambda e: play_next(vc))
    else:
        is_playing = False

@bot.command(name = 'play', help = 'Joins the vc of the person issuing the command, plays and queues songs. Takes in arguments to be searched on youtube')
async def play(ctx, *args):
    global queue
    global is_playing

    arg_string = ' '.join(args)
    
    author_channel = ctx.author.voice.channel

    if author_channel is None:

        await ctx.send('Connect to a vc')
    else:

        try:
            voice_client = await author_channel.connect()
        except:
            
            voice_client = ctx.voice_client

        song = search(arg_string)
        queue.append(song)

        queued_title = song['title']

        await ctx.send(f'♫ queued {queued_title} ♫')
        await ctx.send(file = discord.File(f'img/{random.choice(buffs)}.png'))
            
        if is_playing == False:
            await ctx.send(f'playing {queued_title}')
            await ctx.send(file = discord.File('img/playing.gif'))
            await play_music(voice_client)

@bot.command(name = 'queued', help = 'displays currently queued up songs if there are any')
async def queued(ctx):
    global queue

    all_titles = ''

    for i in range(0, len(queue)):
        all_titles += str(i + 1) + '. ' + queue[i]['title'] + '\n'

    if all_titles != '':

        c_title = current_playing['title']
        embed = discord.Embed(title = f'Current playing: {c_title}')
        embed.description = all_titles
        await ctx.send(embed = embed)
    
    else:

        await ctx.send('no songs in queue')

@bot.command(name = 'remove', help = 'removes a song from queue, takes in number')
async def remove(ctx, number):
    global queue

    if len(queue) > 1:

        try: 
            queue.pop((int(number) - 1))
            await ctx.invoke(bot.get_command('queued'))

        except:
            await ctx.send('no')
 
    else:

        await ctx.send('no songs in queue')

@bot.command(name = 'current', help = 'dispalys current song')
async def current(ctx):
    global current_playing
    global is_playing

    if current_playing != None:

        c_title = current_playing['title']
        c_url = current_playing['link']

        embed = discord.Embed(title = c_title)
        
        await ctx.send(embed = embed)

    else:

        await ctx.send('nothing playing right now')

@bot.command(name = 'shuffle', help = 'shuffles the current queue of songs')
async def shuffle(ctx):
    global queue
    global is_playing

    if len(queue) > 2:

        random.shuffle(queue)
        await ctx.send('shuffled queue')
        await ctx.invoke(bot.get_command('queued'))

    else:

        await ctx.send('the current queue of songs is too small')


@bot.command(name = 'skip', help = 'skips the current song')
async def skip(ctx):

    ctx.voice_client.stop()
    await play_music(ctx.voice_client)


@bot.command(name = 'disconnect', help = 'disconnects bot from voice channel')
async def disconnect(ctx):
    global is_playing

    is_playing = False
    voice_client = ctx.voice_client

    if voice_client.is_connected():
        await voice_client.disconnect()

@bot.command(name = 'pause', help = 'pauses current song')
async def pause(ctx):

    voice_client = ctx.voice_client

    voice_client.pause()

@bot.command(name = 'resume', help = 'resumes paused song')
async def resume(ctx):

    voice_client = ctx.voice_client

    voice_client.resume()

@bot.command(name = 'clear', help = 'clears queue')
async def clear(ctx):

    global queue
    queue = []
    await ctx.send('queue cleared')

@bot.command(name = 'stop', help = 'stops playing songs, but does not disconnect from voice channel')
async def stop(ctx):
    global is_playing

    voice_client = ctx.voice_client

    voice_client.stop()
    is_playing = False
    


bot.run(token)