import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import textwrap


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Images: Loaded.")

    # Commands
    @commands.command()
    async def exist(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Exist: {text}')
        exist = Image.open('./templates/exist.png')
        draw = ImageDraw.Draw(exist)
        para = textwrap.wrap(text, width=19)
        MAX_W, MAX_H = 450, 250
        font = ImageFont.truetype("cc-astro-city.ttf", 44)

        current_h, pad = 50, 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 460, current_h + 50), line, (0,0,0), font=font)
            current_h += h + pad

        exist.save('exist_generated.png')
        await ctx.send(file=discord.File('exist_generated.png'))

    @commands.command()
    async def jim(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Jim: {text}')
        test = Image.open('./templates/jim.jpg')
        draw = ImageDraw.Draw(test)

        split = text.split('.', 1)
        text_top = split[0]
        text_bot = split[1]

        para_top = textwrap.wrap(text_top, width=21)
        para_bot = textwrap.wrap(text_bot, width=19)
        MAX_W, MAX_H = 250, 150
        font = ImageFont.truetype("cc-astro-city.ttf", 28)

        current_h, pad = 50, 10
        for line in para_top:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 95, current_h), line, (0, 0, 0), font=font)
            current_h += h + pad

        current_h, pad = 450, 10
        for line in para_bot:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 70, current_h), line, (0, 0, 0), font=font)
            current_h += h + pad

        test.save('jim_generated.jpg')
        await ctx.send(file=discord.File('jim_generated.jpg'))

    @commands.command()
    async def uno(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Uno: {text}')
        test = Image.open('./templates/uno.jpg')
        draw = ImageDraw.Draw(test)
        para = textwrap.wrap(text, width=13)
        MAX_W, MAX_H = 150, 90
        font = ImageFont.truetype("cc-astro-city.ttf", 18)

        current_h, pad = 170, 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 80, current_h), line, (0, 0, 0), font=font)
            current_h += h + pad

        test.save('uno_generated.jpg')
        await ctx.send(file=discord.File('uno_generated.jpg'))


def setup(client):
    client.add_cog(Images(client))
