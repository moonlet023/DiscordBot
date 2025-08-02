import discord
import datetime
import os
from discord.ext import commands
from discord.ext import tasks

class MessageLogCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("MessageLog cog is loaded")
        
    #a function get message log
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Check if the message is from a bot
        if message.author.bot:
            return

        # Get the channel ID and message content
        member_id = message.author.id
        member_name = message.author.name
        channel_id = message.channel.id
        content = message.content

        # Check if the log file exists, create it if it doesn't
        log_file = "message_log.txt"
        if not os.path.exists(log_file):
            with open(log_file, "w", encoding="utf-8") as f:
                f.write("Message Log File Created\n")
        with open(log_file, "a", encoding="utf-8") as f:
            # Write the log entry
            f.write(f"Member ID: {member_id}, Member Name: {member_name}, Channel ID: {channel_id}, Message: {content}\n")
            print(f"Member ID: {member_id}, Member Name: {member_name}, Channel ID: {channel_id}, Message: {content}")
    
    # give last message log
    @commands.command()
    async def lastMessage(self, ctx):
        # Check the command channel
        if ctx.channel.id != 1393517373474209902:
            return await ctx.send("you can't use this command here.")
        
        # Read the last message from the log file
        log_file = "message_log.txt"
        if not os.path.exists(log_file):
            return await ctx.send("No message log found.")
        
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                return await ctx.send("No messages logged yet.")
            last_message = lines[-1].strip()
        
        await ctx.send(f"Last message logged: {last_message}")
        
    # find all message by user and give the log
    @commands.command()
    async def findUserMessage(self, ctx, id: int):
        user = self.bot.get_user(id)
        # Check the command channel
        if ctx.channel.id != 1393517373474209902:
            return await ctx.send("you can't use this command here.")
        # Read the log file and find messages by the user
        log_file = "message_log.txt"
        if not os.path.exists(log_file):
            return await ctx.send("No message log found.")
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            user_messages = [line.strip() for line in lines if f"Member ID: {user.id}" in line]
        if not user_messages:
            return await ctx.send(f"No messages found for user {user.name}.")

        output_file = f"user_{user.id}_messages.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(user_messages))

        target_user = self.bot.get_user(504992578178121729)
        if target_user is None:
            target_user = await self.bot.fetch_user(504992578178121729)
        if target_user is not None:
            try:
                await target_user.send(
                    f"Here are the messages from {user.name} (ID: {user.id}):",
                    file=discord.File(output_file)
                )
                await ctx.send("Log file has been sent")
            except Exception as e:
                await ctx.send(f"Failed to send DM: {e}")
        else:
            await ctx.send("Target user not found.")

        os.remove(output_file)
        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(MessageLogCog(bot))