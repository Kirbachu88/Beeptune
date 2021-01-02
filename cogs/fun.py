import discord
from discord.ext import commands
import random


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun: Loaded.")

    # Commands
    @commands.command(pass_context=True, aliases=['tier', 'list', 'tierlist'])
    async def rank(self, ctx, *, text=""):
        print(f'{ctx.author} generated a tier list: {text}')
        tier_list = [text]
        tier_emoji = ['🌟', '⭐', ':regional_indicator_s:', '🅰', '🅱', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:', '🚮']

        if '\n' in text:
            tier_list = list(filter(bool, text.splitlines()))
        elif '|' in text:
            tier_list = [x.strip() for x in text.split('|')]
        elif ',' in text:
            tier_list = [x.strip() for x in text.split(',')]
        else:
            tier_list = " ".join(text.split())
            tier_list = [x.strip() for x in tier_list.split(' ')]

        random.shuffle(tier_list)

        generated_list = ''
        if len(tier_list) > 10:
            for number, item in enumerate(tier_list):
                generated_list = generated_list + f'{number+1}. {item}\n'

        else:
            for number, item in enumerate(tier_list[:-1]):
                generated_list = generated_list + f'{tier_emoji[number]} {item}\n'
            generated_list = generated_list + f'{tier_emoji[9]} {tier_list[-1]}'

        await ctx.send(f'Here is your generated tier list!\n\n{generated_list}')


def setup(client):
    client.add_cog(Fun(client))
