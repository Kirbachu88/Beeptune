import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os


# Capital 'C' in Cog!
class Voice(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice: Loaded.")

    # Aliases = Shorthand/Alternatives for the command
    @commands.command(pass_context=True, aliases=['j', 'joi'])
    async def join(self, ctx):
        # Retrieve voice channel the author is in
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        # If user is in a voice channel and if it's connected to a voice channel already
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        # Uncomment if this is bugged
        # await voice.disconnect()
        #
        # if voice and voice.is_connected():
        #     await voice.move_to(channel)
        # else:
        #     voice = await channel.connect()

        print(f"Connected to {channel}.")
        await ctx.send(f"Joined {channel}.")

    @commands.command(pass_context=True, aliases=['l', 'gtfo'])
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Disconnected from {channel}.")
            await ctx.send(f"Left {channel}.")
        else:
            print("Told to leave channel, but was not in one.")
            await ctx.send("I don't think I'm in a voice channel 🤔")

    @commands.command(pass_context=True, aliases=['p'])
    async def play(self, ctx, url: str):
        # Set to True/False
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("Removed old song file.")
        except PermissionError:
            print("Trying to delete song file, but it's being played/in use.")
            await ctx.send("Error: Audio is playing")
            return

        # Downloading using youtube_dl

        await ctx.send("Getting everything ready...")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        # Setting YouTube download options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now...")
            ydl.download([url])

        # Change the name of the song file
        # ./ = Current directory
        for file in os.listdir("./"):
            if file.endswith('.mp3'):
                name = file
                print(f"Renamed File: {file}")
                os.rename(file, "song.mp3")

        # Do a "small function" after playing
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        # Do not go above 0.5
        voice.source.volume = 0.07

        # new name, not always accurate
        nname = name.rsplit("-", 2)
        await ctx.send(f"Playing {nname[0]}")
        print("Playing...")

    @commands.command(pass_context=True, aliases=['wait'])
    async def pause(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Audio paused.")
            voice.pause()
            await ctx.send("Audio paused.")
        else:
            print("No audio playing.")
            await ctx.send("No audio playing, failed to pause.")

    @commands.command(pass_context=True, aliases=['r', 'res'])
    async def resume(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            print("Audio resumed.")
            voice.resume()
            await ctx.send("Audio resumed.")
        else:
            print("Audio is not paused.")
            ctx.send("Audio is not paused.")

    @commands.command(pass_context=True, aliases=['s', 'stfu'])
    async def stop(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            print("Audio stopped!")
            voice.stop()
            await ctx.send("Audio stopped!")
        else:
            print("No audio playing, failed to stop.")
            await ctx.send("No audio playing, failed to stop.")


def setup(client):
    client.add_cog(Voice(client))
