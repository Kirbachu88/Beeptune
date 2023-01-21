import asyncio
import aiohttp
import discord
import os
from discord.ext import commands, tasks

# def get_prefix(bot, message):
#     prefixes = ['b! ', 'b!', 'B! ', 'B!']
#
#     if not message.guild:
#         return 'b!'
#
#     return commands.when_mentioned_or(*prefixes)(bot, message)


class Beeptune(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='b!', case_insensitive=True, intents=intents)
        self.initial_extensions = [
            'cogs.admin_settings',
            'cogs.bgm',
            'cogs.fun',
            'cogs.images',
            'cogs.info'
        ]

    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
    async def background_task(self):
        print('Running background task...')

    async def on_ready(self):
        print('Ready!')


intents = discord.Intents.default()
intents.message_content = True

bot = Beeptune()
bot.run('bot token goes here', reconnect=True)


async def main():
    async with aiohttp.ClientSession() as session:
        async with bot:
            bot.session = session
            await bot.start('token')

asyncio.run(main())

# intents = discord.Intents.default()
# intents.message_content = True
# bot = commands.Bot(intents=intents, command_prefix=get_prefix, case_insensitive=True)


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
    'cooldown': commands.Cooldown(2, 7.0)
    # 2, 7.0, commands.BucketType.user
}

# bot.help_command = CustomHelp()
# CustomHelp(command_attrs=attributes)


# @client.command()
# @commands.check(is_owner)
# async def cogs(ctx, extension):
# @client.command()
# @commands.check(is_owner)
# async def startup(ctx):
#     for filename in os.listdir('./cogs'):
#         if filename.endswith('.py'):
            # Remove the last 3 characters to get rid of '.py'
            # client.load_extension(f'cogs.{filename[:-3]}')
            # await client.add_cog(Info(client))
