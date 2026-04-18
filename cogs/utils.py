import io
import discord
import pandas as pd
from discord.ext import commands
from sqlalchemy import text
from db import engine, db_ready, mask_ip


class Utils(commands.Cog):
    # Utility commands for exporting data and getting help

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='export')
    async def export(self, ctx):
        # Pulls the full incident log and sends it as a csv file attachment
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                df = pd.read_sql("SELECT * FROM incident_logs ORDER BY timestamp DESC", conn)

            if df.empty:
                await ctx.send("No data to export.")
                
                return
            
            df['src_ip'] = df['src_ip'].apply(mask_ip)
            # Write the csv to memory so we don't need to touch the disk
            buffer = io.StringIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)

            await ctx.send(
                content="Here is your incident log export:",
                file=discord.File(fp=io.BytesIO(buffer.getvalue().encode()), filename="incident_logs.csv")
            )

        except Exception as e:
            await ctx.send(f"Export failed: {e}")

    @commands.command(name='help')
    async def help_command(self, ctx):
        # Lists all available commands with a short description
        embed = discord.Embed(title="CPT IDS Query - Commands", color=discord.Color.blue())
        embed.description = (
            "!summary - Overview of total incidents, unique IPs, and top port\n"
            "!top-ports - Top 10 most targeted ports\n"
            "!flags <flag> - Filter incidents by TCP flag, e.g. `!flags S`\n"
            "!flagstats - Breakdown of all TCP flag types\n"
            "!peak-hours - Hours of the day with the most traffic\n"
            "!peak-days - Days of the week with the most traffic\n"
            "!traffic-over-time - Incident counts over the last 24 periods\n"
            "!port-info <port> - Look up what a port is used for\n"
            "!export - Download the full incident log as a CSV"
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Utils(bot))