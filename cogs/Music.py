import asyncio

import discord
import youtube_dl
import os
import random
from discord.ext import commands


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
    'aloop=-1:2e+09'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def j(self, ctx):
        """Joins a voice channel"""
        user = ctx.message.author
        channel = user.voice.channel
        await channel.connect()

    @commands.command()
    async def play(self, ctx):
        """Plays a file from the local filesystem"""
        metronomes = ["80.mp3", "108.mp3", "125.mp3",
                      "140.mp3", "160.mp3", "174.mp3", "208.mp3"]
        query = random.choice(metronomes)
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(
            'Player error: %s' % e) if e else None)

        await ctx.send('{} metronome started for 30 seconds!'.format(query))
#
  #  @commands.command()
  #  async def yt(self, ctx, *, url):
  #      """Plays from a url (almost anything youtube_dl supports)"""
#
  #      async with ctx.typing():
  #          player = await YTDLSource.from_url(url, loop=self.client.loop)
  #          ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#
  #      await ctx.send('Now playing: {}'.format(player.title))
#
  #  @commands.command()
  #  async def stream(self, ctx, *, url):
  #      """Streams from a url (same as yt, but doesn't predownload)"""
  #      ffmpeg_options = {
  #          'options': '-vn -ss 40 -SSEOF 45'
  #      }
  #      async with ctx.typing():
  #          player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
  #          ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#
  #
  #      await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the client from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    # @yt.before_invoke
    # @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


def setup(client):
    client.add_cog(Music(client))
