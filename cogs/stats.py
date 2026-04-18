import discord
from discord.ext import commands
from sqlalchemy import text
from db import engine, db_ready


class Stats(commands.Cog):
    # Commands focused on general traffic statistics

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='summary')
    async def summary(self, ctx):
        # Shows a quick overview of total incidents, unique IPs, and the most hit port
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                total = conn.execute(text("SELECT COUNT(*) FROM incident_logs")).scalar()
                unique_ips = conn.execute(text("SELECT COUNT(DISTINCT src_ip) FROM incident_logs")).scalar()
                top_port = conn.execute(text(
                    "SELECT dst_port FROM incident_logs GROUP BY dst_port ORDER BY COUNT(*) DESC LIMIT 1"
                )).scalar()

            embed = discord.Embed(title="Incident Summary", color=discord.Color.blue())
            embed.add_field(name="Total Incidents", value=str(total), inline=True)
            embed.add_field(name="Unique Source IPs", value=str(unique_ips), inline=True)
            embed.add_field(name="Most Targeted Port", value=str(top_port), inline=True)
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")

    @commands.command(name='top-ports')
    async def top_ports(self, ctx):
        # Shows the top 10 most frequently targeted destination ports
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT dst_port, COUNT(*) as hits FROM incident_logs GROUP BY dst_port ORDER BY hits DESC LIMIT 10"
                ))
                rows = result.fetchall()

            if not rows:
                await ctx.send("No data found.")
                return

            embed = discord.Embed(title="Top Targeted Ports", color=discord.Color.orange())
            table = "\n".join([f"Port `{r.dst_port}` - {r.hits} hits" for r in rows])
            embed.description = table
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")

    @commands.command(name='flagstats')
    async def flagstats(self, ctx):
        # Shows a breakdown of how often each tcp flag type appears in the log
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT tcp_flags, COUNT(*) as count FROM incident_logs GROUP BY tcp_flags ORDER BY count DESC"
                ))
                rows = result.fetchall()

            if not rows:
                await ctx.send("No data found.")
                return

            embed = discord.Embed(title="TCP Flag Breakdown", color=discord.Color.purple())
            table = "\n".join([f"`{r.tcp_flags}` - {r.count} incidents" for r in rows])
            embed.description = table
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")


async def setup(bot):
    await bot.add_cog(Stats(bot))