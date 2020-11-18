import discord
from discord.ext import commands


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Info: Loaded.")

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def marco(self, ctx):
        await ctx.send(f'Polo! {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def info(self, ctx):
        await ctx.send("Descriptive words")

    @commands.command()
    async def server(self, ctx):
        name = str(ctx.guild.name)
        description = str(ctx.guild.description)
        if description == "None":
            description = "No description"

        owner = str(ctx.guild.owner)
        server_id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        member_count = str(ctx.guild.member_count)

        icon = str(ctx.guild.icon_url)

        # Creating a fancy embed
        embed = discord.Embed(
            title=name + " Server Information",
            description=description,
            color=discord.Color.gold()
        )
        embed.set_thumbnail(url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=server_id, inline=True)
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Member Count", value=member_count, inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
