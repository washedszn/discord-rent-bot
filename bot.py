import discord
import os
import json
from discord import app_commands
from discord.ext import tasks
from scraper import nederwoon
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Load config
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

config = load_config()
CHANNEL_ID = config['CHANNEL_ID']
CHECK_INTERVAL = config['CHECK_INTERVAL_SECONDS']
CITY = config['CITY']

# Helper to update config
def update_config(key, value):
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    config[key] = value
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    # Reload the local variables after updating the config
    global CHANNEL_ID, CHECK_INTERVAL, CITY
    config = load_config()
    CHANNEL_ID = config['CHANNEL_ID']
    CHECK_INTERVAL = config['CHECK_INTERVAL_SECONDS']
    CITY = config['CITY']

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
    print('Tree synced')

    check_listings.start()

@tree.command(name='set-channel', description='Set notification channel')
async def set_channel_command(interaction):
    channel_id = interaction.channel_id
    update_config('CHANNEL_ID', channel_id)
    await interaction.response.send_message(f'Set the notification channel to <#{channel_id}>')
    start_or_restart_check_listings()

@tree.command(name='set-city', description='Set the desired city for scraping')
async def set_city_command(interaction, city: str):
    update_config('CITY', city)
    await interaction.response.send_message(f'Set the city to {city}')
    start_or_restart_check_listings()

@tree.command(name='set-interval', description='Set the interval for checking listings (For safety there is a minimum of 60 seconds)')
async def set_interval_command(interaction, interval: int):
    if interval < 60:
        interval = 60
        await interaction.response.send_message('For safety, the minimum interval is 60 seconds. Setting the check interval to 60 seconds.')
    else:
        await interaction.response.send_message(f'Set the check interval to {interval} seconds')
    update_config('CHECK_INTERVAL_SECONDS', interval)
    start_or_restart_check_listings()

def start_or_restart_check_listings():
    if check_listings.is_running():
        check_listings.restart()
    else:
        check_listings.start()

@tasks.loop(seconds=CHECK_INTERVAL)
async def check_listings():
    config = load_config()
    # Ensure config values exist
    if not (config.get('CHANNEL_ID') and config.get('CHECK_INTERVAL_SECONDS') and config.get('CITY')):
        print("Incomplete config. Please ensure all settings are specified.")
        check_listings.stop()
        return
    
    properties = nederwoon()

    for property_data in properties:
        await send_embed(property_data)

async def send_embed(property_data):
    channel = client.get_channel(CHANNEL_ID)
    
    # Create a new embed object
    embed = discord.Embed(
        title=property_data['title'],
        url=property_data['url'],
        color=discord.Color.blue()
    )
    
    # Set the first image as the main image
    embed.set_image(url=property_data['images'][0])
    
    # Add each attribute as a field
    embed.add_field(name="Address", value=property_data['address'], inline=True)
    embed.add_field(name="Property Type", value=property_data['property_type'], inline=True)
    embed.add_field(name="Build Status", value=property_data['build_status'], inline=True)
    embed.add_field(name="Price", value=property_data['price'], inline=True)

    # Send the embed to the channel
    await channel.send(embed=embed)

client.run(DISCORD_TOKEN)
