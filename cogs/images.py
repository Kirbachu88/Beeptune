import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
from io import BytesIO
import requests
import textwrap
import re


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Images: Loaded.")

    # Commands
    @commands.command()
    async def cloud(self, ctx):
        string = str(ctx.message.content)
        string_slice = string[8:]
        url = ctx.message.author.avatar_url

        has_mention = re.match(r'<@!?(\d+)>', string_slice)
        is_url = re.match(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)', string_slice)

        if has_mention:
            url = ctx.message.mentions[0].avatar_url
        elif is_url:
            url = string_slice

        print(f'{ctx.author} generated with Cloud: {url}')
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((150, 150))
        # img = ImageOps.grayscale(img)

        im_a = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(im_a)
        draw.rectangle((0, 0, 150, 150), fill=255)

        im_a = im_a.rotate(20, resample=Image.BILINEAR, expand=True)
        img = img.rotate(20, resample=Image.BILINEAR, expand=True)

        cloud = Image.open('./templates/cloud.png')
        cloud.paste(img, (425, 413), im_a)
        cloud.save('cloud_generated.png')
        await ctx.message.delete()
        await ctx.send(file=discord.File('cloud_generated.png'))

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
            draw.text((((MAX_W - w) / 2) + 460, current_h + 50), line, (0, 0, 0), font=font)
            current_h += h + pad

        exist.save('exist_generated.png')
        await ctx.send(file=discord.File('exist_generated.png'))

@commands.command()
    async def jim(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Jim: {text}')
        test = Image.open('./templates/jim.jpg')
        draw = ImageDraw.Draw(test)

        text_top = text
        text_bot = ''

        if re.match(r'.*\..*', text):
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
