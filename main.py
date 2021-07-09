import os
from dotenv import load_dotenv
import discord

# Setup the .env file
load_dotenv()

# Setup client
client = discord.Client()
token = os.environ["DISCORD_BOT_TOKEN"]


@client.event
async def on_ready():
    print(f"The bot has started as {client.user}")

client.run(token)
