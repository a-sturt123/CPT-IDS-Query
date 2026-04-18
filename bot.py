import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot with the ! prefix and enable message content reading
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# List of cog files to load on startup
COGS = [
    'cogs.stats',
    'cogs.time',
    'cogs.lookup',
    'cogs.utils',
]


@bot.event
async def on_ready():
    # Fires when the bot successfully connects to discord
    print(f"[SUCCESS] Logged in as {bot.user}")


async def main():
    # Load each cog then start the bot
    async with bot:
        for cog in COGS:
            try:
                await bot.load_extension(cog)
                print(f"[SUCCESS] Loaded {cog}")
            except Exception as e:
                print(f"[WARNING] Failed to load {cog}: {e}")
        await bot.start(TOKEN)


if __name__ == "__main__":
    if not TOKEN:
        print("[ERROR] DISCORD_TOKEN not found in .env file!")
        exit(1)
    asyncio.run(main())