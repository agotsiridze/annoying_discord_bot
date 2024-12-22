import os
import random
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv

from html_parser import Parser
from timer import set_timer

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SOUNDS_URL = os.getenv("SOUNDS_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


parser = Parser(SOUNDS_URL)
parser.download_soup()


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    bot.loop.create_task(random_play())


async def random_play():
    while True:
        try:
            wait_time = random.randint(150, 900)
            # await asyncio.sleep(wait_time)
            await set_timer(wait_time)
            channel_id = int(CHANNEL_ID)
            guild = bot.guilds[0]
            voice_channel = discord.utils.get(guild.voice_channels, id=channel_id)
            voice_client = await voice_channel.connect()
            ffmpeg_options = {
                "options": "-vn",  # Disable video
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",  # Handle network issues
            }
            link = parser.get_link()
            audio_source = discord.FFmpegPCMAudio(link, **ffmpeg_options)
            voice_client.play(
                audio_source,
                after=lambda e: print(f"Playback error: {e}") if e else None,
            )
            while voice_client.is_playing():
                await asyncio.sleep(1)
            await voice_client.disconnect()
        except Exception as e:
            print(f"Error during random playback: {e}")


bot.run(TOKEN)
