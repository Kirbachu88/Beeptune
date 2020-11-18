import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='b!')


def is_owner(ctx):
    return ctx.author.id == 'Your Discord ID'


@client.command()
@commands.check(is_owner)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Loaded.")


@client.command()
@commands.check(is_owner)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("Unloaded.")


@client.command()
@commands.check(is_owner)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("Done.")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        # Remove the last 3 characters to get rid of '.py'
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('bot token goes here')
