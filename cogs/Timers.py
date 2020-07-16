import discord
from discord.ext import commands
import asyncio
from asyncio import sleep, TimerHandle
import discord.user
import discord.member
from discord.utils import get
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice


class EventTimer(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    stopTimer = False

    @commands.command()
    async def stoptimer(self, ctx):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global stopTimer
            stopTimer = True
            embed = discord.Embed(title="TIMER STOPPED", color=0xf55742)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    @commands.command()
    async def timer(self, ctx, seconds):
        if discord.utils.get(ctx.message.author.roles, name="Host") or discord.utils.get(ctx.message.author.roles, name="BBXINT Staff"):
            global stopTimer
            stopTimer = False
            try:
                secondint = int(seconds)
                if secondint < 0 or secondint == 0:
                    await ctx.send("Can't go lower than 0 seconds!")
                else:
                    embed = discord.Embed(
                        title=seconds + " SECONDS ON THE CLOCK", color=0x7289da)
                    await ctx.send(embed=embed)
                    while True:
                        secondint = secondint - 1
                        if secondint == 0:
                            embed = discord.Embed(
                                title="TIME", color=0xf55742)
                            await ctx.send(embed=embed)
                            break
                        await asyncio.sleep(1)
                        if secondint == 120:
                            embed = discord.Embed(
                                title="120 Seconds Left", color=0xaaf542)
                        if secondint == 105:
                            embed = discord.Embed(
                                title="105 Seconds Left", color=0xaaf542)
                        if secondint == 90:
                            embed = discord.Embed(
                                title="90 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 75:
                            embed = discord.Embed(
                                title="75 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 60:
                            embed = discord.Embed(
                                title="60 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 45:
                            embed = discord.Embed(
                                title="45 Seconds Left", color=0xf57e42)
                            await ctx.send(embed=embed)
                        if secondint == 30:
                            embed = discord.Embed(
                                title="30 Seconds Left", color=0xf57e42)
                            await ctx.send(embed=embed)
                        if secondint == 15:
                            embed = discord.Embed(
                                title="15 Seconds Left", color=0xf55742)
                            await ctx.send(embed=embed)
                        if stopTimer == True:
                            secondint = 0
            except ValueError:
                await ctx.send("Must be a number!")
        else:
            embed = discord.Embed(
                title=('This command is only for the Host!'), color=0xf55742)
            await ctx.send(embed=embed)

    """__________________Timer for Everyone__________________"""
    stopTimer2 = False

    @commands.command()
    async def stoptime(self, ctx):
        global stopTimer2
        stopTimer2 = True
        embed = discord.Embed(title="TIMER STOPPED", color=0xf55742)
        await ctx.send(embed=embed)

    @commands.command()
    async def time(self, ctx, seconds):
        global stopTimer2
        stopTimer2 = False
        print(ctx.channel.id)
        if ctx.channel.id == 691699079838826496:
            print('YES!')
            try:
                secondint = int(seconds)
                if secondint < 0 or secondint == 0:
                    await ctx.send("Can't go lower than 0 seconds!")
                else:
                    embed = discord.Embed(
                        title=seconds + " SECONDS ON THE CLOCK", color=0x7289da)
                    await ctx.send(embed=embed)
                    while True:
                        secondint = secondint - 1
                        if secondint == 0:
                            embed = discord.Embed(
                                title="TIME", color=0xf55742)
                            await ctx.send(embed=embed)
                            break
                        await asyncio.sleep(1)
                        if secondint == 120:
                            embed = discord.Embed(
                                title="120 Seconds Left", color=0xaaf542)
                        if secondint == 105:
                            embed = discord.Embed(
                                title="105 Seconds Left", color=0xaaf542)
                        if secondint == 90:
                            embed = discord.Embed(
                                title="90 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 75:
                            embed = discord.Embed(
                                title="75 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 60:
                            embed = discord.Embed(
                                title="60 Seconds Left", color=0xaaf542)
                            await ctx.send(embed=embed)
                        if secondint == 45:
                            embed = discord.Embed(
                                title="45 Seconds Left", color=0xf57e42)
                            await ctx.send(embed=embed)
                        if secondint == 30:
                            embed = discord.Embed(
                                title="30 Seconds Left", color=0xf57e42)
                            await ctx.send(embed=embed)
                        if secondint == 15:
                            embed = discord.Embed(
                                title="15 Seconds Left", color=0xf55742)
                            await ctx.send(embed=embed)
                        if stopTimer2 == True:
                            secondint = 0
            except ValueError:
                await ctx.send("Must be a number!")
        else:
            text_channel = self.client.get_channel(691699079838826496)
            await ctx.send(f"{ctx.author.mention}, The **!time** command is for **Friendly Battles** and can **only** be used in {text_channel.mention}!")
            print('NOOOOOOOOOO!')


def setup(client):
    client.add_cog(EventTimer(client))
