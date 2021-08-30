import discord
from discord.ext import commands
from discord.utils import get
import os

ost_path = 'C:/Users/USERNAME/Music/OST/'


class BGM(commands.Cog):

    time = "day"

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("BGM: Loaded.")

    # Aliases = Shorthand/Alternatives for the command
    @commands.command(aliases=['t', 'time'], help="Changes \"Time of day\" for DPPt OST")
    async def settime(self, ctx, new_time=""):
        new_time = new_time.lower()
        if new_time in ['d', 'day', 'daytime']:
            BGM.time = 'day'
        elif new_time in ['n', 'night', 'nighttime']:
            BGM.time = 'night'
        await ctx.send(f'Time is set to {BGM.time}.')

    @commands.command(aliases=['bg', 'playfile', 'ost'], help="I will try to play this song in our files!")
    async def bgm(self, ctx, *, filename: str):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if BGM.time == 'day':
            ost_dir = f'{ost_path}Day/'
            await ctx.send("Searching in Day...")
        elif BGM.time == 'night':
            ost_dir = f'{ost_path}Night/'
            await ctx.send("Searching in Night...")

        found, name = find_file(self, filename, ost_dir)

        if not found:
            await ctx.send("Song not found in Day/Night, searching OST Folder...")
            ost_dir = ost_path
            found, name = find_file(self, filename, ost_dir)
        if not found:
            await ctx.send(f'Could not find a song with this title :(\n> {filename}')
        else:
            if voice and voice.is_playing():
                print("Audio stopped!")
                voice.stop()
                await ctx.send("Audio stopped!")

            # Do a "small function" after playing
            voice.play(discord.FFmpegPCMAudio(f'{ost_dir}{name}'), after=lambda e: print(f"{name} has finished playing"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            # Do not go above 0.5
            voice.source.volume = 0.07

            # new name, not always accurate
            nname = name.rsplit("-", 2)
            await ctx.send(f"Playing {nname[0]}")
            print("Playing...")

    @commands.command(aliases=['playlist', 'ostlist'], help="Gives a list of all songs available.")
    async def songlist(self, ctx):
        ost_list = []
        append_list(self, ost_list, f'{ost_path}Day')
        append_list(self, ost_list, ost_path)
        await ctx.send('\n'.join(ost_list))


def append_list(self, ost_list, ost_dir):
    for file in os.listdir(f'{ost_dir}'):
        nname = file.rsplit("-", 2)
        ost_list.append(f'{nname[0]}')


def find_file(self, filename, ost_dir):
    found = False
    name = ''

    for file in os.listdir(f'{ost_dir}'):
        if file.endswith('.mp3') and filename.lower() in file.lower():
            found = True
            name = file
            break
    return found, name


def setup(client):
    client.add_cog(BGM(client))
