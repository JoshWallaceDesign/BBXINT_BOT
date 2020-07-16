import discord
from discord.ext import commands
import asyncio
from discord.utils import get
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


class VoteSystem(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(name='vote', aliases=['judge', 'battle', 'vs'])
    async def vote(self, ctx, attempter):
        global judges
        global name1
        global name2
        judges = 0
        name1 = ''
        name2 = ''
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "creds.json", scope)
        gsheet = gspread.authorize(creds)
        sheet = gsheet.open("leaderboard").sheet1

        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check

        try:
            attempt = int(attempter)
            if attempt != 3 and attempt != 5:
                await ctx.send('There must be 3 or 5 judges.')
                raise BaseException
            if attempt == '':
                await ctx.send('Please enter the amount of judges (Example: ,vs 3)')
                raise BaseException
            if attempt is None:
                await ctx.send('Please enter the amount of judges (Example: ,vs 3)')
                raise BaseException
            while True:
                if attempt == 5:
                    judges = 5
                    break
                if attempt == 3:
                    judges = 3
                    break
        except:
            await ctx.send('oof, must be a number.')
            return

        await ctx.send('Please enter the name of the first beatboxer')
        msg = await self.client.wait_for('message', check=check(ctx.author), timeout=30)
        name1 = msg.content
        await ctx.send('Please enter the name of the second beatboxer')
        msg = await self.client.wait_for('message', check=check(ctx.author), timeout=30)
        name2 = msg.content
        embed = discord.Embed(
            title=(f'**{name1}** vs **{name2}!**'), description=(f'Total Judges:{judges} 🗳️\nReact to this message to vote!\n☝️ to vote for **{name1}**\n✌ to vote for **{name2}**\n🙅‍♂️ to vote for Overtime'), color=0x7289da)
        embed.set_author(name="BATTLE TIME!", url="https://www.beatboxinternational.com",
                         icon_url="https://scontent.flhr3-2.fna.fbcdn.net/v/t1.0-9/p960x960/94872982_1594119310744042_2467931763544948736_o.jpg?_nc_cat=100&_nc_sid=85a577&_nc_ohc=UR1CBk-wn6UAX_H4pCU&_nc_ht=scontent.flhr3-2.fna&_nc_tp=6&oh=1b46baa33d2cc4a819715690c90e0d7b&oe=5F1E5D6D")
        msg1 = await ctx.send(embed=embed)

        channel = msg1.channel
        choices = {"☝️": f'{name1}',
                   "✌": f"{name2}",
                   "🙅‍♂️": "Overtime"}

        for choice in choices:
            await msg1.add_reaction(choice)  # add the bot reactions

        await asyncio.sleep(15)

        try:  # Wait 1 minute for any reaction
            while True:
                # fetch the message again
                msg1 = await channel.fetch_message(msg1.id)
                reaction1 = get(msg1.reactions, emoji='☝️')
                reaction2 = get(msg1.reactions, emoji='✌')
                reaction3 = get(msg1.reactions, emoji='🙅‍♂️')
                if reaction1.count >= 2:  # judges / 2 + 1:
                    embed = discord.Embed(title=(f' **{name1} wins this battle! 🏆 **'), description=(
                        f'Leaderboard points:\n {reaction1.count - 1} for **{name1}**!\n{reaction2.count - 1} for **{name2}**!'), color=0x7289da)
                    embed.set_author(name="THE RESULTS ARE IN!", url="https://www.beatboxinternational.com",
                                     icon_url="https://scontent.flhr3-2.fna.fbcdn.net/v/t1.0-9/p960x960/94872982_1594119310744042_2467931763544948736_o.jpg?_nc_cat=100&_nc_sid=85a577&_nc_ohc=UR1CBk-wn6UAX_H4pCU&_nc_ht=scontent.flhr3-2.fna&_nc_tp=6&oh=1b46baa33d2cc4a819715690c90e0d7b&oe=5F1E5D6D")
                    await ctx.send(embed=embed)
                    insertRow = [name1, reaction1.count]
                    if not sheet.findall(f"{name1}"):
                        sheet.append_row(insertRow, table_range='A2')
                    else:
                        cell = sheet.find(f"{name1}")
                        row_number = cell.row
                        print(cell.row)
                        workbook2_row = 'B'+str(row_number)
                        print(workbook2_row)
                        print(reaction1.count)
                        val = sheet.acell(f'{workbook2_row}').value
                        print(val)
                        sheet.update_acell(
                            workbook2_row, (f'=SUM({val}+{reaction1.count})'))
                    break
                    return
                elif reaction2.count >= 2:  # judges / 2 + 1:
                    embed = discord.Embed(
                        title=(f'**{name2} wins this battle! 🏆**'), color=0x7289da)
                    embed.set_author(name="THE RESULTS ARE IN!", url="https://www.beatboxinternational.com",
                                     icon_url="https://scontent.flhr3-2.fna.fbcdn.net/v/t1.0-9/p960x960/94872982_1594119310744042_2467931763544948736_o.jpg?_nc_cat=100&_nc_sid=85a577&_nc_ohc=UR1CBk-wn6UAX_H4pCU&_nc_ht=scontent.flhr3-2.fna&_nc_tp=6&oh=1b46baa33d2cc4a819715690c90e0d7b&oe=5F1E5D6D")
                    await ctx.send(embed=embed)
                    break
                elif reaction3.count >= 2:  # judges / 2 + 1:
                    embed = discord.Embed(
                        title=(f'**Overtime wins this battle! **'), color=0x7289da)
                    embed.set_author(name="THE RESULTS ARE IN!", url="https://www.beatboxinternational.com",
                                     icon_url="https://scontent.flhr3-2.fna.fbcdn.net/v/t1.0-9/p960x960/94872982_1594119310744042_2467931763544948736_o.jpg?_nc_cat=100&_nc_sid=85a577&_nc_ohc=UR1CBk-wn6UAX_H4pCU&_nc_ht=scontent.flhr3-2.fna&_nc_tp=6&oh=1b46baa33d2cc4a819715690c90e0d7b&oe=5F1E5D6D")
                    await ctx.send(embed=embed)
                    break
                elif reaction1.count == 2 and reaction2.count == 2 and reaction3.count == 2:
                    embed = discord.Embed(
                        title=(f"**It's a split decision, wins this battle! 🏆**"), color=0x7289da)
                    embed.set_author(name="THE RESULTS ARE IN!", url="https://www.beatboxinternational.com",
                                     icon_url="https://scontent.flhr3-2.fna.fbcdn.net/v/t1.0-9/p960x960/94872982_1594119310744042_2467931763544948736_o.jpg?_nc_cat=100&_nc_sid=85a577&_nc_ohc=UR1CBk-wn6UAX_H4pCU&_nc_ht=scontent.flhr3-2.fna&_nc_tp=6&oh=1b46baa33d2cc4a819715690c90e0d7b&oe=5F1E5D6D")
                    await ctx.send(embed=embed)
                    break
                else:
                    embed = discord.Embed(
                        title=f"Oof, judges set to {judges}. Waiting 30 seconds for more votes.")
                    await ctx.send(embed=embed)
                    await asyncio.sleep(15)
        except:
            await ctx.send('Sorry, there was an error. I am now dead ⚰️ Please get the votes manually for this battle or try again.')
            return


def setup(client):
    client.add_cog(VoteSystem(client))
