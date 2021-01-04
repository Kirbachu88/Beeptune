import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageSequence
from io import BytesIO
import requests
import textwrap
import re


async def write_text(text_split, template, name, font_size, color, current_w, current_h, pad_w=0, pad_h=0, max_w=0):
    draw = ImageDraw.Draw(template)
    font = ImageFont.truetype("cc-astro-city.ttf", font_size)
    if max_w == 0:
        for line in text_split:
            draw.text((current_w, current_h), line, color, font=font)
            current_w += pad_w
            current_h += pad_h
    else:
        for line in text_split:
            w, h = draw.textsize(line, font=font)
            draw.text((((max_w - w) / 2) + current_w, current_h), line, color, font=font)
            current_w += pad_w
            current_h += pad_h
    template.save(f'./generated/{name}')


class Images(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Images: Loaded.")

    # Commands
    @commands.command()
    async def button(self, ctx, *, text=""):
        split = ['']
        if '\n' in text:
            split = list(filter(bool, text.splitlines()))
        elif '|' in text:
            split = [x.strip() for x in text.split('|')]
        else:
            split[0] = text

        color = (0, 0, 0)
        font_size = 35
        max_w = 0
        if len(split) < 2:
            name = 'button.jpg'
            color = (255, 255, 255)
            max_w = 200
            current_w, pad_w, current_h, pad_h = 70, 0, 270, 0
        elif len(split) == 2:
            name = 'button2.jpg'
            font_size = 35
            max_w = 200
            current_w, pad_w, current_h, pad_h = 55, 215, 120, -40
        else:
            name = 'button4.jpg'
            current_w, pad_w, current_h, pad_h = 120, 0, 40, 105

        template = Image.open(f'./templates/{name}')
        await write_text(split, template, name, font_size, color, current_w, current_h, pad_w, pad_h, max_w)

        print(f'{ctx.author} generated with Button: {text}')
        await ctx.send(file=discord.File(f'./generated/{name}'))

    @commands.command()
    async def cloud(self, ctx):
        string = str(ctx.message.content)
        string_slice = string[8:]
        url = ctx.message.author.avatar_url

        has_mention = re.match(r'<@!?(\d+)>', string_slice)
        is_url = re.match(r'(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|jpeg|gif|png)', string_slice)

        if has_mention:
            url = ctx.message.mentions[0].avatar_url
        elif is_url:
            url = string_slice

        # Creating a mask
        im_a = Image.new("L", (150, 150), 0)
        draw = ImageDraw.Draw(im_a)
        draw.rectangle((0, 0, 150, 150), fill=255)
        im_a = im_a.rotate(20, resample=Image.BILINEAR, expand=True)

        # Retrieving images
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((150, 150))

        template = Image.open('./templates/cloud.png')

        if str(url).endswith('.gif'):
            frames = []
            for frame in ImageSequence.Iterator(img):
                frame = frame.copy()
                frame = frame.rotate(20, resample=Image.BILINEAR, expand=True)
                template.paste(frame, (425, 413), im_a)
                frames.append(template)
            frames[0].save('./generated/cloud.gif', save_all=True, append_images=frames[1:], optimize=False, loop=0)
            await ctx.message.delete()
            await ctx.send(file=discord.File('./generated/cloud.gif'))
        else:
            print(f'{ctx.author} generated with Cloud: {url}')

            img = img.rotate(20, resample=Image.BILINEAR, expand=True)

            template.paste(img, (425, 413), im_a)
            template.save('./generated/cloud.png')
            await ctx.message.delete()
            await ctx.send(file=discord.File('./generated/cloud.png'))

    @commands.command()
    async def exist(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Exist: {text}')
        template = Image.open('./templates/exist.png')
        draw = ImageDraw.Draw(template)
        para = textwrap.wrap(text, width=19)
        MAX_W, MAX_H = 450, 250
        font = ImageFont.truetype("cc-astro-city.ttf", 44)

        current_h, pad = 50, 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 460, current_h + 50), line, (0, 0, 0), font=font)
            current_h += h + pad

        template.save('./generated/exist.png')
        await ctx.send(file=discord.File('./generated/exist.png'))

    @commands.command()
    async def jim(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Jim: {text}')
        template = Image.open('./templates/jim.jpg')
        draw = ImageDraw.Draw(template)

        text_top = text
        text_bot = ''

        if '|' in text:
            split = text.split('|', 1)
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

        template.save('./generated/jim.jpg')
        await ctx.send(file=discord.File('./generated/jim.jpg'))

    @commands.command()
    async def uno(self, ctx, *, text=""):
        print(f'{ctx.author} generated with Uno: {text}')
        template = Image.open('./templates/uno.jpg')
        draw = ImageDraw.Draw(template)
        para = textwrap.wrap(text, width=13)
        MAX_W, MAX_H = 150, 90
        font = ImageFont.truetype("cc-astro-city.ttf", 18)

        current_h, pad = 170, 10
        for line in para:
            w, h = draw.textsize(line, font=font)
            draw.text((((MAX_W - w) / 2) + 80, current_h), line, (0, 0, 0), font=font)
            current_h += h + pad

        template.save('./generated/uno.jpg')
        await ctx.send(file=discord.File('./generated/uno.jpg'))


def setup(client):
    client.add_cog(Images(client))
