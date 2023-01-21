import discord
from discord.ext import commands
import random
import textwrap


class Fun(commands.Cog, name='fun'):
    def __init__(self, client):
        self.client = client

    # New async cog_load special method is automatically called
    async def cog_load(self):
        print("Fun: Loaded.")

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun: Ready!")

    # Commands
    @commands.command(name='rank', pass_context=True, aliases=['tier', 'list', 'tierlist'])
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

    @commands.command(name='flip', pass_context=True, aliases=['coin', 'coinflip'])
    async def flip(self, ctx, text=""):
        if text.isnumeric():
            count = int(text)
            if count > 100:
                count = 100
            elif count < 1:
                count = 1
        else:
            count = 1

        print(f'{ctx.author} flipped {count} coin(s)')
        samples = [random.randint(1, 2) for _ in range(count)]
        heads = samples.count(1)
        tails = samples.count(2)

        result = ""
        for i in samples:
            result = result + '🌝' if i == 1 else result + '🌑'

        result = textwrap.fill(result, 10)

        # Creating a fancy embed
        embed = discord.Embed(
            title="Coin Flip Results!",
            description=result,
            color=discord.Color.gold()
        )

        if heads > tails:
            result_img = 'https://noto-website-2.storage.googleapis.com/emoji/emoji_u1f315.png'
        elif tails > heads:
            result_img = 'https://noto-website-2.storage.googleapis.com/emoji/emoji_u1f311.png'
        else:
            result_img = 'https://noto-website-2.storage.googleapis.com/emoji/emoji_u1f317.png'

        embed.set_thumbnail(url=result_img)

        if count > 1:
            embed.add_field(name=f'{ctx.message.author.nick} flipped __{count}__ coins!',
                            value=f'It\'s **{heads}** heads to **{tails}** tails!')
        elif heads > tails:
            embed.add_field(name=f'{ctx.message.author.nick} flipped a coin!',
                            value=f'It\'s **heads!**')
        else:
            embed.add_field(name=f'{ctx.message.author.nick} flipped a coin!',
                            value=f'It\'s **tails!**')

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
