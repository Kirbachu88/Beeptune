import discord
from discord.ext import commands


class AdminSettings(commands.Cog):

    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.id == 'Your Discord ID'

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info: Loaded.")

    # Commands
    @commands.command()
    async def status(self, ctx, arg1="", arg2="", arg3=""):
        verb = str(arg1)
        noun = str(arg2)
        url = str(arg3)
        if verb == "playing":
            # Setting `Playing ` status
            await self.client.change_presence(activity=discord.Game(name=noun))
            await ctx.send("Now " + verb + " " + noun)
        elif verb == "watching":
            # Setting `Watching ` status
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=noun))
            await ctx.send("Now " + verb + " " + noun)
        elif verb == "streaming":
            # Setting `Streaming ` status
            await self.client.change_presence(activity=discord.Streaming(name=noun, url=url))
            await ctx.send("Now " + verb + " " + noun + " at " + url)
        elif verb == "listening":
            # Setting `Listening ` status
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=noun))
            await ctx.send("Now " + verb + " to " + noun)
        elif verb == "competing":
            # Setting `Competing in` status
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name=noun))
            await ctx.send("Now " + verb + " in " + noun)
        else:
            await self.client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name="your every move"))
            await ctx.send("Using default status!")


def setup(client):
    client.add_cog(AdminSettings(client))
