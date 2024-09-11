import discord
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
from typing import Final

# Load environment variables from a .env file
load_dotenv()

TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



# API URL for football matches
API_URL = "https://a082-138-229-215-91.ngrok-free.app/matches"

# Function to fetch matches for a specific date and optional league
async def fetch_matches_for_date(date, league=None):
    url = f"{API_URL}?date={date}"
    print(url)
    try:
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        return "Error fetching data."

    if not data:
        return f"No matches available for {date}."

    if league:
        matches = data.get(league, [])
    else:
        matches = []
        for league_matches in data.values():
            matches.extend(league_matches)

    if matches:
        response = f"Matches for {date}:\n"
        for match in matches:
            response += f"{match['home_team']} vs {match['away_team']} at {match['time']}\n"
    else:
        response = f"No matches available for {date}."
    print(response)
    return response

# Validate date format
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$start'):
        await message.channel.send(
            "Use the following commands to get football matches:\n"
            "`$today_matches` - Get matches for today\n"
            "`$date YYYY-MM-DD` - Get matches for a specific date\n"
            "`$league league_name` - Get matches for a specific league today (e.g., `!league Premier League`)"
        )
    
    if msg.startswith('$today_matches'):
        today = datetime.now().strftime("%Y-%m-%d")
        response = await fetch_matches_for_date(today)
        await message.channel.send(response)
    
    if msg.startswith('$date'):
        date = msg.split('$date ', 1)[1]
        if not validate_date(date):
            await message.channel.send("Invalid date format. Use YYYY-MM-DD.")
            return
        
        response = await fetch_matches_for_date(date)
        await message.channel.send(response)
    
    if msg.startswith('$league'):
        league_name = msg.split('$league ', 1)[1]
        today = datetime.now().strftime("%Y-%m-%d")
        response = await fetch_matches_for_date(today, league_name)
        await message.channel.send(response)

# Start the bot with the token from the environment variable
if TOKEN is None:
    print("Error: TOKEN environment variable is not set.")
else:
    client.run(TOKEN)
