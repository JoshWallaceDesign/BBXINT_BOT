import discord
from asyncio import sleep, TimerHandle
import random
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


"""__________________Google Sheets__________________"""
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

gclient = gspread.authorize(creds)

sheet = gclient.open("BBXINT_JUDGING").worksheet(
    'PARTICIPANTS')  # Open the spreadhseet
sheet2 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 1')  # Open the spreadhseet
sheet3 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 2')  # Open the spreadhseet
sheet4 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 3')  # Open the spreadhseet
sheet5 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 4')  # Open the spreadhseet\
sheet6 = gclient.open("BBXINT_JUDGING").worksheet(
    'JUDGE 5')  # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records


"""__________________Prefix__________________"""

client = commands.Bot(command_prefix='!')

"""__________________Timer__________________"""
stopTimer = False


@client.command()
async def stop(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global stopTimer
        stopTimer = True
        embed = discord.Embed(title="TIMER STOPPED", color=0xf55742)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)


@client.command()
async def timer(ctx, seconds):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
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


@client.command()
async def ping(ctx):
    await ctx.send(f'PongPo! {round(client.latency) *1000}ms')

"""CoinFlip"""


@client.command()
async def flip(ctx):
    choices = ["It's Heads", "It's Tails from Portugal"]
    randcoin = random.choice(choices)
    embed = discord.Embed(
        title=(randcoin), color=0x7289da)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print('Missing Input')

"""_______________________Queue System Start_______________________"""

parts = {}
que = {}
locked = False

"""__________________Join & Leave__________________"""


@client.command()
async def join(ctx):
    if locked == False:
        global parts
        global que
        if discord.utils.get(ctx.message.author.roles, name="Participant"):

            print('in queue')
            embed = discord.Embed(
                title=("You are already in the Queue! If it doesn't show you in the Queue," + '\n' + "then !leave & !join again!"), color=0xf55742)
            await ctx.send(embed=embed)

        else:
            member = ctx.author
            role = discord.utils.get(member.guild.roles, name="Participant")
            await discord.Member.add_roles(member, role)
            print('not in queue')
            part = ctx.message.author.display_name
            insertRow = [part]
            if not sheet.findall(part):
                sheet.append_row(insertRow, table_range='A2')
            else:
                print('found a match')
            parts = part

            if id in que:
                que[id].append(part)
            else:
                que[id] = [part]

            embed = discord.Embed(
                title=(part + ' has been Added to the Queue'), color=0xaaf542)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title=('The Queue is Locked!'), color=0xf55742)
        await ctx.send(embed=embed)


@client.command()
async def leave(ctx):
    global parts
    member = ctx.author
    nick = ctx.message.author.display_name
    print(nick)
    role = discord.utils.get(member.guild.roles, name="Participant")
    await discord.Member.remove_roles(member, role)
    x = ctx.message.author.display_name
    print('Position', x)
    embed = discord.Embed(
        title=(ctx.message.author.display_name + ' has left the Queue!'), color=0xf55742)
    await ctx.send(embed=embed)
    part = que[id].remove(x)
    parts = part

"""__________________Queue__________________"""


@client.command()
async def queue(ctx):

    if len(que) <= 0:
        embed = discord.Embed(
            title=('Queue is Empty!' + '\n' + '!join to Part'), color=0xf55742)
        await ctx.send(embed=embed)
    else:

        amount = len(que[id])
        print(amount)
        queholder = que[id]
        embed = discord.Embed(
            title=('Participants | ' + str(amount)), color=0x7289da)
        await ctx.send(embed=embed)
        await ctx.send('LIST:' + '\n' + ("\n".join(que[id])))
        if len([que]) == 0:
            print('Queue Empty')
        else:
            performingnow = queholder[0]
            embed = discord.Embed(
                title=('Now | ' + performingnow), color=0xaaf542)
            await ctx.send(embed=embed)


"""__________________Add & Kick for Host Only__________________"""


@ client.command()
async def add(ctx, member: discord.Member):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global parts
        global que
        part = member.display_name
        role = discord.utils.get(member.guild.roles, name="Participant")
        await discord.Member.add_roles(member, role)
        insertRow = [part]
        if not sheet.findall(part):
            sheet.append_row(insertRow, table_range='A2')
        else:
            print('found a match')
        parts = part
        if id in que:
            que[id].append(part)
        else:
            que[id] = [part]
        embed = discord.Embed(
            title=(part + ' has been Added to the Queue'), color=0xaaf542)
        await ctx.send(embed=embed)
    else:
        await ctx.send('This command is only for the Host!')


@ client.command()
async def kick(ctx, member: discord.Member):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global parts
        role = discord.utils.get(member.guild.roles, name="Participant")
        await discord.Member.remove_roles(member, role)
        x = member.display_name
        print('Position', x)
        part = que[id].remove(x)
        parts = part
        embed = discord.Embed(
            title=(x + ' has been kicked from the Queue!'), color=0xf55742)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)

"""__________________Lock & Unlock for Host Only__________________"""


@ client.command()
async def lock(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global locked
        locked = True
        embed = discord.Embed(
            title=('The Queue is now Locked!'), color=0xf55742)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)


@ client.command()
async def unlock(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global locked
        locked = False
        embed = discord.Embed(
            title=('The Queue is now Unlocked!'), color=0xaaf542)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)

"""__________________Next, Skip, & End for Host Only__________________"""


@ client.command()
async def next(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        global parts
        part = que[id].pop(0)
        parts = part
        queholder = que[id]
        performingnow = queholder[0]
        amount = len(que[id])
        embed = discord.Embed(
            title=('Up Next | ' + performingnow), color=0xaaf542)
        await ctx.send(embed=embed)
        await ctx.send('LIST:' + '\n' + ("\n".join(que[id])))
        embed = discord.Embed(
            title=('Participants | ' + str(amount)), color=0x7289da)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)


@ client.command()
async def skip(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        queholder = que[id]
        x = queholder[0]
        embed = discord.Embed(
            title=(x + ' has been skiped!'), color=0xf55742)
        await ctx.send(embed=embed)
        que[id].append(que[id].pop(que[id].index(x)))

        performingnow = queholder[0]
        amount = len(que[id])
        embed = discord.Embed(
            title=('Up Next | ' + performingnow), color=0xaaf542)
        await ctx.send(embed=embed)
        await ctx.send('LIST:' + '\n' + ("\n".join(que[id])))
        embed = discord.Embed(
            title=('Participants | ' + str(amount)), color=0x7289da)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)


@ client.command()
async def end(ctx):
    if discord.utils.get(ctx.message.author.roles, name="Host"):
        que.clear()
        embed = discord.Embed(
            title=('The Event is now Over!'), color=0x7289da)
        await ctx.send(embed=embed)
        role_to_remove = "Participant"
        for user in ctx.guild.members:
            for role in user.roles:
                if role.name == role_to_remove:
                    await user.remove_roles(role)

    else:
        embed = discord.Embed(
            title=('This command is only for the Host!'), color=0xf55742)
        await ctx.send(embed=embed)


@ client.command()
async def resetsheet(ctx):
    range_of_cells = sheet.range('A2:A151')
    for cell in range_of_cells:
        cell.value = ''
    sheet.update_cells(range_of_cells)
    range_of_cells = sheet2.range('B3:F152')
    for cell in range_of_cells:
        cell.value = ''
    sheet2.update_cells(range_of_cells)
    range_of_cells = sheet3.range('B3:F152')
    for cell in range_of_cells:
        cell.value = ''
    sheet3.update_cells(range_of_cells)
    range_of_cells = sheet4.range('B3:F152')
    for cell in range_of_cells:
        cell.value = ''
    sheet4.update_cells(range_of_cells)
    range_of_cells = sheet5.range('B3:F152')
    for cell in range_of_cells:
        cell.value = ''
    sheet5.update_cells(range_of_cells)
    range_of_cells = sheet6.range('B3:F152')
    for cell in range_of_cells:
        cell.value = ''
    sheet6.update_cells(range_of_cells)


@ client.command()
async def dmsheet(ctx):
    await ctx.author.send("Here's the BBXINT Judging Sheet " + '\n' + 'https://docs.google.com/spreadsheets/d/1FAIk6R9Rr12X-DyWlH3Z7vBUV8Ij74qGyTF4n86a66o/edit?usp=sharing')

"""__________________Queue System End__________________"""


@ client.command()
async def commandlist(ctx):
    await ctx.send("Event Commands:" + '\n' + '\n' + "TIMER & FLIP:" + '\n' + "!timer seconds | Timer followed by number of seconds" + '\n' + "!stop | Stops Timer" + '\n' + "!flip | Flips a coin" + '\n' + '\n' + "QUEUE:" + '\n' + "!join | Join Queue" + '\n' + "!leave | Leave Queue" + '\n' + "!queue | Show Queue" + '\n' + "Host Only:" +
                   '\n' + "!next | Next in Queue" + '\n' + "!skip | Skips to end of Queue" + '\n' + "!add @member | Adds @member to Queue" + '\n' + "!kick @member | Kicks @member from Queue" + '\n' + "!lock | Locks Queue" + '\n' + "!unlock | Unlocks Queue" + '\n' + "!end | Ends Event & Clears Queue")


@ client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('BEATBOX INTERNATIONAL'))
    print('Bot is Online')

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client.run(token)
