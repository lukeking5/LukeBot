import discord
from discord.ext import commands
import random
import time
from datetime import datetime
import pytz

random.seed(time.time())
class CoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f"Hey There, {ctx.author.mention}!")
        
    @commands.command() # kiss someone!
    async def kiss(self, ctx, user: discord.Member): # Kiss another member!
        await ctx.send(f"{ctx.author.mention} kisses {user.mention}!")
        await ctx.send("https://media1.tenor.com/m/bD7CkL3ACK4AAAAd/good-morning.gif")
        
    @commands.command() # punch someone!
    async def punch(self, ctx, user: discord.Member): # Punch another member!
        await ctx.send(f"{ctx.author.mention} punches {user.mention}!")
        await ctx.send("https://media1.tenor.com/m/jwGSFHGRyFUAAAAC/boxing-tom-and-jerry.gif")
        
    @commands.command()
    async def help(self, ctx): # list of all commands
        await ctx.author.send("Here are some useful '*' Commands:\n"
        "Hello: Hey There!\n"
        "Time: Get current time in U.S. Timezones"
        "RTD: Rolls a 6 sided die\n"
        "GIF YourTextHere: Receive a random gif with your own prompt!\n"
        "KISS @member: Kiss another member of the server!\n"
        "PUNCH @member: Punch another member of the server!\n"
        "TypeRace: Begin a typing race!\n")
        await ctx.send("Check your DM's for a comprehensive help section.")
        
    @commands.command()
    async def time(self, ctx):
        await ctx.send(f"PST: {datetime.now(pytz.timezone("America/Los_Angeles")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"MST: {datetime.now(pytz.timezone("America/Denver")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"CST: {datetime.now(pytz.timezone("America/Chicago")).strftime("%Y-%m-%d %I:%M:%S %p")}\n"
                       f"EST: {datetime.now(pytz.timezone("America/New_York")).strftime("%Y-%m-%d %I:%M:%S %p")}\n")
    @commands.command()
    async def rtd(self, ctx):
        await ctx.send(file=discord.File(f'assets/dice/DIE_0{random.randint(1,6)}.png'))

async def setup(bot):
    await bot.add_cog(CoreCommands(bot))