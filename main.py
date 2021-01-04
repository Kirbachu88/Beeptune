import discord
import os
from discord.ext import commands

def get_prefix(bot, message):
    prefixes = ['b! ', 'b!', 'B! ', 'B!']

    if not message.guild:
        return 'b!'

    return commands.when_mentioned_or(*prefixes)(bot, message)


client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)


class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(
                title='A very helpful embed!',
                description=page,
                color=discord.Color.gold()
            )
            await destination.send(embed=embed)


attributes = {
    'aliases': ['halp'],
    'cooldown': commands.Cooldown(2, 7.0, commands.BucketType.user)
}

client.help_command = CustomHelp(command_attrs=attributes)


def is_owner(ctx):
    return ctx.author.id == 'Your Discord ID'


@client.event
async def on_command_error(ctx, error):
    error = getattr(error, "original", error)
    if isinstance(error, commands.ExtensionNotFound):
        error = 'Couldn\'t find that!'
    elif isinstance(error, commands.ExtensionAlreadyLoaded):
        error = 'Already loaded that!'
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'You\'re going too fast! (Wait {str(error)[-5:]})', delete_after=5)
        return
    await ctx.send(error)


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
