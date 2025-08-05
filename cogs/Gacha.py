import discord
from discord.ext import commands
from discord import app_commands
import random

class Gacha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="singlegacha", description="單抽轉蛋")
    async def singlegacha(self, interaction: discord.Interaction):
        probabilities = {
            "common": 0.5,
            "rare": 0.3,
            "epic": 0.15,
            "legendary": 0.04,
            "mythic": 0.01
        }
        emjois = {
            "common": "⚪",
            "rare": "🔵",
            "epic": "🟢",
            "legendary": "🟡",
            "mythic": "🟣"
        }
        random_value = random.random()
        cumulative_probability = 0.0
        result = None
        for item, probability in probabilities.items():
            cumulative_probability += probability
            if random_value < cumulative_probability:
                result = item
                break
        await interaction.response.send_message(f"你抽到了 {emjois[result]} {result}")
        
    @app_commands.command(name="multigacha", description="十連抽轉蛋")
    async def multigacha(self, interaction: discord.Interaction):
        results = []
        for _ in range(10):
            probabilities = {
                "common": 0.5,
                "rare": 0.3,
                "epic": 0.15,
                "legendary": 0.04,
                "mythic": 0.01
            }
            emjois = {
                "common": "⚪",
                "rare": "🔵",
                "epic": "🟢",
                "legendary": "🟡",
                "mythic": "🟣"
            }
            random_value = random.random()
            cumulative_probability = 0.0
            result = None
            for item, probability in probabilities.items():
                cumulative_probability += probability
                if random_value < cumulative_probability:
                    result = item
                    break
            results.append(f"{emjois[result]} {result}")
        await interaction.response.send_message(" ".join([r.split()[0] for r in results]))
        await interaction.followup.send("你抽到了: " + ", ".join(results))
        
    @app_commands.command(name="機率", description="轉蛋機率")
    async def gacha_probability(self, interaction: discord.Interaction):
        probabilities = {
            "common": 0.5,
            "rare": 0.3,
            "epic": 0.15,
            "legendary": 0.04,
            "mythic": 0.01
        }
        emjois = {
            "common": "⚪",
            "rare": "🔵",
            "epic": "🟢",
            "legendary": "🟡",
            "mythic": "🟣"
        }
        probability_message = "\n".join([f"{emjois[item]} {item}: {probability * 100:.2f}%" for item, probability in probabilities.items()])
        await interaction.response.send_message(f"轉蛋機率:\n{probability_message}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Gacha(bot))