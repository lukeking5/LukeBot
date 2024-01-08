import discord
from discord import app_commands
from discord.ext import commands
import random
import time
from datetime import datetime
import pytz
from databases.databases import cmdToDB

random.seed(time.time())
class CoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.hybrid_command(name="hello", description="Hey there!")
    async def hello(self, ctx):
        """Hey there!"""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id))
        
        await ctx.send(f"Hey there, {ctx.author.mention}!")
        
    @commands.hybrid_command(name="kiss", description="Kiss someone!")
    async def kiss(self, ctx, user: discord.Member): # Kiss another member!
        """Kiss someone!"""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id), str(user.id))
        
        await ctx.send(f"{ctx.author.mention} kisses {user.mention}!")
        await ctx.send("https://media1.tenor.com/m/bD7CkL3ACK4AAAAd/good-morning.gif")
        
    @commands.hybrid_command(name = "punch", description="Punch someone!")
    async def punch(self, ctx, user: discord.Member): # Punch another member!
        """Punch someone!"""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id), str(user.id))
        
        await ctx.send(f"{ctx.author.mention} punches {user.mention}!")
        await ctx.send("https://media1.tenor.com/m/jwGSFHGRyFUAAAAC/boxing-tom-and-jerry.gif")
        
    @commands.hybrid_command(name="time", description="Get the time in U.S. time zones.")
    async def time(self, ctx):
        """Get the time in U.S. time zones."""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id))
        
        await ctx.send(f"PST: {datetime.now(pytz.timezone("America/Los_Angeles")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"MST: {datetime.now(pytz.timezone("America/Denver")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"CST: {datetime.now(pytz.timezone("America/Chicago")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"EST: {datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p")}\n")
        
    @commands.hybrid_command(name="rtd", description="Roll the dice.")
    async def rtd(self, ctx):
        """Roll the dice."""    
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id))
        
        await ctx.send(file=discord.File(f'assets/dice/DIE_0{random.randint(1,6)}.png'))

async def setup(bot):
    await bot.add_cog(CoreCommands(bot))