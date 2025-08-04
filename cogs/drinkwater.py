import discord
import datetime
from discord.ext import commands, tasks

class Drinkwater(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_sent_hour = None
        self.water.start()
        print("Drinkwater cog loaded.")

    @tasks.loop(minutes=1)
    async def water(self):
        now = datetime.datetime.now()
        target_hours = [0, 3, 6, 9, 12, 15, 18, 21]
        if now.minute == 0 and now.hour in target_hours:
            if self.last_sent_hour != now.hour:
                channel = self.bot.get_channel(1394068448702759097)
                guild = self.bot.get_guild(1392733155898818652)
                role = guild.get_role(1401596211814731816) if guild else None
                if channel and role:
                    mention = role.mention
                    await channel.send(f"{mention} 飲水時間到")
                    self.last_sent_hour = now.hour
                else:
                    print("Channel or role not found for sending role message.")

    @water.before_loop
    async def before_water(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def dw(self, ctx):
        channel = self.bot.get_channel(1394068448702759097)
        guild = self.bot.get_guild(1392733155898818652)
        role = guild.get_role(1401596211814731816) if guild else None
        if channel and role:
            mention = role.mention
            await channel.send(f"{mention} 飲水時間到")
        else:
            await ctx.send("Channel or role not found for sending role message.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Drinkwater(bot))
    print("Drinkwater cog setup complete.")