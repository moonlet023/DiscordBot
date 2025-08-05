import discord
import datetime
import os
from discord.ext import commands
from discord.ext import tasks
import yt_dlp
import asyncio

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.song_queue = asyncio.Queue()
        self.play_next_song = asyncio.Event()
        self.current_voice_client = None
        self.looping = False
        self.volume = 0.5
        self.bot.loop.create_task(self.player_loop())
        print("Music cog is loaded")
        
    APIKEY = 'AIzaSyD1Yy9rcmIcJtaPrvaMIWqqBYd0DnHaupA'
    
    voice_clients = {}  # Dictionary to keep track of voice clients
    current_voice_client = None
    volume = 0.5  # Default volume level
    
    @commands.command()
    async def musicHelp(self, ctx, len: str):
        help_message_en = (
            "Music Commands:\n"
            "`!join` - Join your voice channel\n"
            "`!leave` - Leave the voice channel\n"
            "`!play <url>` - Play a song from a URL\n"
            "`!loop` - Toggle looping of the current song\n"
            "`!stop` - Stop the current song\n"
            "`!volume <level>` - Set the volume (0-100)\n"
            "`!clean` - Clear the song queue\n"
            "`!list_songs` - List all songs in the queue\n"
            "`!listCreate` - Create a song list\n"
            "`!listAdd <list_name> <url>` - Add a song to a song list\n"
            "`!listShow <list_name>` - Show songs in a song list\n"
            "`!listplay <listname>` - Play songs from a song list\n"
            "`!listDelete <list_name>` - Delete a song list\n"
            )
        help_message_zh = (
            "音樂指令:\n"
            "`!join` - 加入你的語音頻道\n"
            "`!leave` - 離開語音頻道\n"
            "`!play <url>` - 播放歌曲\n"
            "`!loop` - 切換當前歌曲循環播放\n"
            "`!stop` - 停止當前歌曲\n"
            "`!volume <level>` - 設置音量 (0-100)\n"
            "`!clean` - 清空歌曲隊列\n"
            "`!list_songs` - 列出所有歌曲\n"
            "`!listCreate` - 創建歌曲列表\n"
            "`!listAdd <list_name> <url>` - 向歌曲列表添加歌曲\n"
            "`!listShow <list_name>` - 顯示歌曲列表中的歌曲\n"
            "`!listplay <listname>` - 播放歌曲列表中的歌曲\n"
            "`!listDelete <list_name>` - 刪除歌曲列表\n"
            )
        
        if len == "en":
            await ctx.send(help_message_en)
        elif len == "zh":
            await ctx.send(help_message_zh)
        elif len == None:
            await ctx.send(help_message_en)
        else:
            await ctx.send(help_message_en)
            
        
    # join voice channel command
    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
            self.current_voice_client = await voice_channel.connect()
            await ctx.send(f"Joined voice channel: {voice_channel.name}")
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
    
    # leave voice channel command
    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            print("Left voice channel")
        else:
            await ctx.send("need connected to any voice channel.")
    
    # play music command with yt-dlp
    @commands.command()
    async def play(self, ctx, *, url):
        if not ctx.voice_client:
            voice_channel = ctx.author.voice.channel
            self.current_voice_client = await voice_channel.connect()
            await ctx.send(f"Joined voice channel: {voice_channel.name}")
        
        #check the url is not a playlist
        if "start_radio" in url:
            return await ctx.send("playlist 唔可以播放，請使用單曲link")
        else:
            if "list" in url:
                return await ctx.send("playlist 唔可以播放，請使用單曲link")
            else:
        
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'default_search': 'auto',
                    'source_address': '0.0.0.0'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_url = info['url']
                    title = info.get('title', 'Unknown Title')

                await self.song_queue.put((audio_url, title, ctx))
                await ctx.send(f"Added to queue: {title}")
    @commands.command()
    async def listplay(self, ctx, *, listname: str):
        file_path = f"./songlists/{listname}.json"
        if not os.path.exists(file_path):
            return await ctx.send(f"Song list '{listname}' does not exist.")
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            song_list = json.load(f)
        if not song_list["songs"]:
            await ctx.send(f"Song list '{listname}' is empty.")
        else:
            for song in song_list["songs"]:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'quiet': True,
                    'no_warnings': True,
                    'default_search': 'auto',
                    'source_address': '0.0.0.0'
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(song, download=False)
                    audio_url = info['url']
                    title = info.get('title', 'Unknown Title')
                await self.song_queue.put((audio_url, title, ctx))
                await ctx.send(f"Added to queue: {title}")
                

    # loop music command
    @commands.command()
    async def loop(self, ctx):
        
        self.looping = not self.looping
        status = "true" if self.looping else "flase"
        await ctx.send(f"looping is {status}")

    # stop music command
    @commands.command()
    async def stop(self, ctx):
        if not ctx.voice_client:
           voice_channel = ctx.author.voice.channel
           self.current_voice_client = await voice_channel.connect()
           await ctx.send(f"Joined voice channel: {voice_channel.name}")
        
        ctx.voice_client.stop()
        await ctx.send("Stopped playing music.")
    
    # list all song
    @commands.command()
    async def list_songs(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("need connected to a voice channel.")
        
        
        
        # This is a placeholder for the actual song list
        # You would need to implement a way to keep track of songs
        await ctx.send("Available songs:\n" + "\n".join(self.song_queue))
        
    # set bot volume
    @commands.command()
    async def volume(self, ctx, volume: float):
        if not ctx.voice_client:
            return await ctx.send("need connected to a voice channel.")
        if volume < 0 or volume > 100:
            return await ctx.send("Volume must be between 0 and 100.")
        new_volume = volume / 100.0
        self.volume = new_volume
    
        if ctx.voice_client.source:
            ctx.voice_client.source.volume = new_volume
        await ctx.send(f"Volume set to {volume}%")
        
    # clear the song queue
    @commands.command()
    async def clean(self, ctx):
        if not ctx.voice_client:
            return await ctx.send("need connected to a voice channel.")
        while not self.song_queue.empty():
            await self.song_queue.get()
        await ctx.send("Song queue cleared.")
    
    # player loop to play songs from the queue
    async def player_loop(self):
        while True:
            audio_url, title, ctx = await self.song_queue.get()
            voice_client = ctx.voice_client
            if not voice_client:
                continue

            def after_playing(error):
                self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

            source = discord.FFmpegPCMAudio(
                audio_url,
                before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                options='-vn'
            )
            
            source = discord.PCMVolumeTransformer(source, volume=self.volume)
            voice_client.play(source, after=after_playing)
            
            await self.play_next_song.wait()
            self.play_next_song.clear()

            if self.looping:
                await self.song_queue.put((audio_url, title, ctx))
                
async def setup(bot: commands.Bot):
    await bot.add_cog(Music(bot))
    print("Music cog setup complete")
