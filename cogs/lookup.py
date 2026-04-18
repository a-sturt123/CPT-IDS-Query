import discord
from discord.ext import commands
from sqlalchemy import text
from db import engine, db_ready


# Common port names used by the port-info command
PORT_INFO = {
    21: "FTP - File Transfer Protocol",
    22: "SSH - Secure Shell",
    23: "Telnet - Unencrypted remote access",
    25: "SMTP - Email sending",
    53: "DNS - Domain Name System",
    80: "HTTP - Unencrypted web traffic",
    443: "HTTPS - Encrypted web traffic",
    445: "SMB - Windows file sharing",
    3306: "MySQL - Database",
    3389: "RDP - Remote Desktop Protocol",
    5432: "PostgreSQL - Database",
    8080: "HTTP Alternate - Often used for proxies or dev servers",
}


class Lookup(commands.Cog):
    # Commands for filtering and looking up specific traffic details

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='flags')
    async def flags(self, ctx, flag: str = None):
        # Filters incidents by a specific TCP flag, e.g. !flags S for SYN
        if not db_ready():
            await ctx.send("No database connection available yet.")
            return

        if not flag:
            await ctx.send("Usage: `!flags <flag>` — e.g. `!flags S` for SYN traffic")
            return

        try:
            with engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT timestamp, dst_port FROM incident_logs WHERE tcp_flags LIKE :flag ORDER BY timestamp DESC LIMIT 20"
                ), {"flag": f"%{flag}%"})
                rows = result.fetchall()

            if not rows:
                await ctx.send(f"No incidents found with flag `{flag}`.")
                return

            embed = discord.Embed(title=f"Incidents with Flag: {flag}", color=discord.Color.purple())
            table = "\n".join([f"`{r.timestamp}` | Port {r.dst_port}" for r in rows])
            embed.description = table
            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"Query failed: {e}")

    @commands.command(name='port-info')
    async def port_info(self, ctx, port: int = None):
        # Looks up what a given port number is commonly used for
        if not port:
            await ctx.send("Usage: `!port-info <port>` — e.g. `!port-info 443`")
            return

        info = PORT_INFO.get(port, "No information available for that port.")
        embed = discord.Embed(title=f"Port {port}", color=discord.Color.blue())
        embed.description = info
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Lookup(bot))