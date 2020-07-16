import discord
from discord.ext import commands
import asyncio
import discord.user
from discord.utils import get
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice


class HelpEvents(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command(name="help", aliases=['info', 'helpme'])
    async def paginate(self, ctx):
        text_channel = self.client.get_channel(691699079838826496)
        embeds = [
            discord.Embed(title=f"Timer Commands - Prefix = !",
                          description=f"**EVENT TIMER**\n!timer (time) = Start the timer(eg: !timer 90)\n!stop = Stop the timer\n\n**FRIENDLY TIMER**\n!time (time) = Start the time(eg: !time 90)\n!stoptime = Stop the time\n Can only be used in {text_channel.mention}\n\n**FLIP COMMAND**\n!flip = Flips a coin", color=0x7289da),
            discord.Embed(title="Event Commands - Prefix = !",
                          description="**EVENT QUEUE**\n!join = Joins the queue\n!leave = Leaves the queue\n!queue = Shows the queue\n**HOST & STAFF ONLY**\n!next = Next in the queue\n!skip = Skips to the end of the queue\n!add (@someone) | Adds someone to the queue (eg: !add @member)\n!kick (@someone) | Removes someone to the queue (eg: !kick @member)\n!lock = Locks the queue\n!unlock = Unlocks the queue\n!close (Channel) = Locks the channel (eg. !close #eventchat)\n!open (Channel) = Opens the channel (eg. !open #eventchat)\n!end = Ends the event and clears the queue\n**JUDGING SHEETS**\nHost Only\n!dmsheet = DMs the Judging sheet to the host\n!resetsheet = Resets the sheet for the next event", color=0x7289da),
            discord.Embed(title=f"🔴 Send a video 🎥",
                          description="**Want to feature on our YouTube channel?**\n\n1. Find a quiet place, with no background noise\n\n2. Make sure your camera is filming landscape/sideways/horizontally\n\n3. Say your name and where you're from - then drop some fire for at least 90 seconds!\n\n4. Head to beatboxinternational.com, or send your video to beatboxinternational@gmail.com\n\n", color=0x7289da),
            discord.Embed(title="Credits",
                          description="This bot was made by T-Pot from the UK 🇬🇧 and STeaMie from Namibia 🇳🇦\nCheck us out on Instagram @steam.esh and @t.pot__\nwww.beatboxinternational.com", color=0x7289da)
        ]
        paginator = BotEmbedPaginator(ctx, embeds)
        await paginator.run()


def setup(client):
    client.add_cog(HelpEvents(client))
