import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Set up Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('gskey.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1D5lw3LKoHSdMt6ccsMzjLSJbA6xwgLN3QJbVfXSUa9Y').worksheet('Orders')

# Set up the bot
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True  # Enable guild intents for slash commands

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

    # Sync bot commands
    try:
        synced = await bot.tree.sync()
        print(f"Synchronised {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name='create', description='Create a logistics order')
@app_commands.describe(item="The item to be ordered", quantity="The quantity of the item", region="The region for the order", region_zone="The zone within the region", facility="The facility for the order", description="A description of the order")
async def create(interaction:discord.Interaction, item: str, quantity: int, region: str, region_zone: str, facility: str, description: str):
    # Check if the sheet has a header row, else append a header row
    if not sheet.row_values(1):
        sheet.update('A1:G1', [['ID', 'Item', 'Quantity', 'Region', 'Region Zone', 'Facility', 'Description']])
    # Generate a unique ID for the order
    order_id = len(sheet.col_values(1)) + 1

    # Append data to Google Sheet with the generated ID
    sheet.append_row([order_id, item, quantity, region, region_zone, facility, description])
    await interaction.response.send_message(f'Logistics order created with ID {order_id}: {item}, {quantity}, {region}, {region_zone}, {facility}, {description}')

@bot.tree.command(name='collect', description='Collect a logistics order')
async def collect(ctx):
    # Logic for collecting logistics order (to be implemented)
    await ctx.respond('Collect command called. Implement logic here.')

# Run the bot
bot.run(os.getenv('DISCORD_BOT_TOKEN'))