import discord
from discord.ext import commands
from datetime import datetime
from discord.ext import tasks

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Ping cog is loaded")
    
    @commands.command()
    async def ping(self, ctx):
        """Check the bot's latency."""
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        await ctx.send(f"Pong! Latency: {latency}ms")
    
    @commands.command()
    async def uptime(self, ctx):
        """Check the bot's uptime."""
        uptime = datetime.now() - self.bot.start_time
        await ctx.send(f"Uptime: {uptime}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
    print("Ping cog has been added to the bot.")