import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import random
from collections import Counter
import youtube_dl
import os
from dotenv import load_dotenv
from discord import FFmpegPCMAudio
from os import system

client = commands.Bot(command_prefix='!', help_command=None)


# client.remove_command('help')


@client.event
async def on_ready():
    print('Im ready for action.')
    return await client.change_presence(activity=discord.Activity(type=3, name='youtube.com/beatboxinternational'))


@client.event
async def on_command_error(ctx, error):
    pass


@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['You suck. So, no.',
                 'You can do it']
    await ctx.send(f'Questions: {question}\n Answers: {random.choice(responses)}')

extensions = ['cogs.HelpEvents',
              'cogs.Music', 'cogs.Timers', 'cogs.BBXEvents']

if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)

'''for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')'''

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client.run(token)
