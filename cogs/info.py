import discord
from discord.ext import commands


class Info(commands.Cog, name='info'):
    def __init__(self, bot):
        self.client = bot

    # New async cog_load special method is automatically called
    async def cog_load(self):
        print("Info: Loaded.")

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info: Ready!")

    # Commands
    @commands.command(name='ping')
    async def ping(self, ctx):
        print("lol")
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command(name='marco')
    async def marco(self, ctx):
        await ctx.send(f'Polo! {round(self.client.latency * 1000)}ms')

    @commands.command(name='info')
    async def info(self, ctx):
        await ctx.send("Descriptive words")

    @commands.command(name='server')
    async def server(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        if description == "None":
            description = "No description"

        owner = str(ctx.guild.owner)
        server_id = str(ctx.guild.id)
        member_count = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon.url)

        # Creating a fancy embed
        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=server_id, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))
