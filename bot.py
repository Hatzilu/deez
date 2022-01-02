import discord
import numpy
import asyncio
from discord import FFmpegPCMAudio
from discord.ext import commands
import os
import youtube_dl
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('BOT_TOKEN')
client = commands.Bot(command_prefix = "deez ")

# @client.event
# @client.event
# async def on_voice_state_update(self, member, before, after):
    
#     voice = discord.utils.get(client.voice_clients, guild=member.guild)
    
#     if after.channel and not before.channel:
#         if voice == None:
#             voice_channel = member.voice.channel
#             # await asyncio.sleep(0.5)
#             vc = await voice_channel.connect()         
#             vc.play(FFmpegPCMAudio('./fart.mp3'))
#             await asyncio.sleep(6)
#             await member.guild.voice_client.disconnect()
@client.command(name = "play",
                pass_context = True)
async def play(ctx, url : str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    #connect to VC if not already 
    try:
        voiceChannel = ctx.author.voice.channel
        await voiceChannel.connect()
    except:
        ctx.send("balls in my face")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        ctx.send('balls')
    for file in os.listdir("./"):
        ctx.send('balls2')
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    ctx.send('playing song deez')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def say(ctx):
    user_message = ctx.message.content.split()
    user_message.pop(0)
    user_message.pop(0)
    await ctx.message.delete()
    await ctx.send(' '.join(user_message))
    print(user_message)

async def on_message(self, message):
    # don't respond to ourselves
    if message.author == self.user or not (message.content.startswith(prefix)):
        return

    #get message args
    args = message.content.split()
    print("args is", args)
    #מה אתה אומר
    test = args.pop(0)
    print("test is", test)
    print("args NOW is", args)
    try:
        command = args[0]
    except:
        command = ''
    print("cmd is", command)
    args = ' '.join(args)
    #מה הוא אומר
    try:
        if command == 'ping':
            await message.channel.send('pong')
        elif command == 'help':
            await message.channel.send('אין עזרה זדיינו')
        elif command == 'nuts':
            await message.channel.send('https://www.youtube.com/watch?v=GHxFr_oDSTI')
        else:
            await message.channel.send('deez what sir')
    except e:
        await message.channel.send('Error \n', e)

client.run(token)