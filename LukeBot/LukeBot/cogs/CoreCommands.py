import discord
from discord.ext import commands
import random
import time

random.seed(time.time())
class CoreCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command()
    async def help(self, ctx):
        await ctx.author.send("Here are some useful '*' Commands:\n"
        "Hello: Hey There!\n"
        "RTD: Rolls a 6 sided die\n"
        "GIF YourTextHere: receive a random gif with your own prompt!")
        await ctx.send("Check your DM's for a comprehensive help section.")
        
    @commands.command()
    async def rtd(self, ctx):
        await ctx.send(file=discord.File(f'assets/dice/DIE_0{random.randint(1,6)}.png'))

async def setup(bot):
    await bot.add_cog(CoreCommands(bot))