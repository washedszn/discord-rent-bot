import discord
import os
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
BASE_URL = os.getenv('BASE_URL')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_SECONDS', 60))  # default to 60 if not set

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}({client.user.id})')
    await tree.sync()
    check_listings.start()

@tasks.loop(seconds=CHECK_INTERVAL)  # Uses the CHECK_INTERVAL from .env (in seconds)
async def check_listings():
    # call web scrapers
    print('run scrapers')
    channel = client.get_channel(0)
    #await channel.send('yo')
    
@tree.command(name='set-channel', description='Set the channel which receives new rental properties')
async def set_channel_command(interaction):
    await interaction.response.send_message('working')

client.run(DISCORD_TOKEN)
