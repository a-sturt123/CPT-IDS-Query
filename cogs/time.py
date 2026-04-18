import discord
from discord.ext import commands
from sqlalchemy import text
from db import engine, db_ready


class Time(commands.Cog):
    # Commands focused on traffic patterns over time

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='peak-hours')
    async def peak_hours(self, ctx):
        # Shows which hours of the day see the most traffic
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT strftime('%H', timestamp) as hour, COUNT(*) as count FROM incident_logs GROUP BY hour ORDER BY count DESC"
                ))
                rows = result.fetchall()

            if not rows:
                await ctx.send("No data found.")
                return

            embed = discord.Embed(title="Peak Traffic Hours", color=discord.Color.green())
            table = "\n".join([f"{r.hour}:00 - {r.count} incidents" for r in rows])
            embed.description = table
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")

    @commands.command(name='peak-days')
    async def peak_days(self, ctx):
        # Shows which days of the week see the most traffic
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        # Map numeric day values to names
        day_names = {"0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday",
                     "4": "Thursday", "5": "Friday", "6": "Saturday"}

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT strftime('%w', timestamp) as day, COUNT(*) as count FROM incident_logs GROUP BY day ORDER BY count DESC"
                ))
                rows = result.fetchall()

            if not rows:
                await ctx.send("No data found.")
                return

            embed = discord.Embed(title="Peak Traffic Days", color=discord.Color.green())
            table = "\n".join([f"{day_names.get(r.day, r.day)} - {r.count} incidents" for r in rows])
            embed.description = table
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")

    @commands.command(name='traffic-over-time')
    async def traffic_over_time(self, ctx):
        # Shows incident counts over the last 24 periods as a simple text bar chart
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT strftime('%Y-%m-%d %H:00', timestamp) as period, COUNT(*) as count FROM incident_logs GROUP BY period ORDER BY period DESC LIMIT 24"
                ))
                rows = result.fetchall()

            if not rows:
                await ctx.send("No data found.")
                return

            # Scale bars relative to the highest count in the results
            max_count = max(r.count for r in rows)
            embed = discord.Embed(title="Traffic Over Time (Last 24 Periods)", color=discord.Color.blue())
            bars = "\n".join([f"`{r.period}` {'|' * int((r.count / max_count) * 20)} {r.count}" for r in rows])
            embed.description = bars
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")


async def setup(bot):
    await bot.add_cog(Time(bot))