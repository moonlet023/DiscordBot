import discord
from discord.ext import commands, tasks
import os

class Songlist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Songlist cog is loaded")
        
    @commands.command()
    async def listCreate(self, ctx, *, name: str):
        # Create a song list in JSON format and save it to a file
        song_list = {"name": name, "songs": []}
        file_path = f"./songlists/{name}.json"
        
        if not os.path.exists("./songlists"):
            os.makedirs("./songlists")
        with open(file_path, 'w', encoding='utf-8') as f:
            import json
            json.dump(song_list, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Song list '{name}' created successfully.")
        
    @commands.command()
    async def listAdd(self, ctx, list_name: str, *, url):
        # Add a song to the specified song list
        file_path = f"./songlists/{list_name}.json"
        if not os.path.exists(file_path):
            return await ctx.send(f"Song list '{list_name}' does not exist.")
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            song_list = json.load(f)
        song_list["songs"].append(url)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(song_list, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Added song to '{list_name}': {url}")
        
    @commands.command()
    async def listShow(self, ctx, list_name: str):
        # Show the songs in the specified song list
        file_path = f"./songlists/{list_name}.json"
        if not os.path.exists(file_path):
            return await ctx.send(f"Song list '{list_name}' does not exist.")
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            song_list = json.load(f)
        if not song_list["songs"]:
            await ctx.send(f"Song list '{list_name}' is empty.")
        else:
            songs = "\n".join(song_list["songs"])
            await ctx.send(f"Songs in '{list_name}':\n{songs}")
            
    @commands.command()
    async def listDelete(self, ctx, list_name: str):
        # Delete the specified song list
        file_path = f"./songlists/{list_name}.json"
        if not os.path.exists(file_path):
            return await ctx.send(f"Song list '{list_name}' does not exist.")
        os.remove(file_path)
        await ctx.send(f"Deleted song list '{list_name}'.")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(Songlist(bot))
    print("Songlist cog setup complete.")