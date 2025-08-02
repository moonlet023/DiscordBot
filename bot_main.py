import os
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import cogs

# verable
tocken = input("input bot token：")
time = datetime.now()

# connect client
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)




# client = discord.Client(intents = intents)

#on ready
@bot.event
async def on_ready():
    print(f"Start On --> {bot.user}")
    print(f"Bot invite link: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="溏心風暴之DC監守者"))
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"load {filename} ")
    slash = await bot.tree.sync()
    print(f"load {len(slash)} slash commands")
    # give bot link

              
#load new cogs
@bot.command()
async def load(ctx, extension):
    # Check the command channel
    if ctx.channel.id != 1393517373474209902:
        return await ctx.send("you can't use this command here.")
    # Check if the extension is already loaded
    if extension in bot.extensions:
        channel = bot.get_channel(1393517373474209902)
        await channel.send(f"{extension} is already loaded.")
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension} done.")
              
#load cogs when it update
@bot.command()
async def reload(ctx, extension):
    # Check the command channel
    if ctx.channel.id != 1393517373474209902:
        return await ctx.send("you can't use this command here.")
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"ReLoaded {extension} done.")
    
#unload cogs
@bot.command()
async def unload(ctx, extension):
    # Check the command channel
    if ctx.channel.id != 1393517373474209902: 
        return await ctx.send("you can't use this command here.")
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"UnLoaded {extension} done.")
    
#temp function
        
@bot.command()
async def sync(ctx):
    if ctx.channel.id != 1393517373474209902:
        return await ctx.send("you can't use this command here.")
    synced = await bot.tree.sync()
    await ctx.send(f" {len(synced)} slash commands synced.")

    
bot.run(tocken)