import random
import time
import requests
from bs4 import BeautifulSoup
from discord.ext import commands

random.seed(time.time())

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def gif(self, ctx, *, arg): # Function for grabbing random gif given string
        arg = arg.replace(' ', '-') # spaces become %20 in image search. ############### LATER SHOULD IMPLEMENT MORE SUCH AS '+' ##############
        gifLinks = []
        #content of search URL
        response = requests.get("https://tenor.com/search/" + arg + "-gifs")
        soup = BeautifulSoup(response.text, "html.parser")
        gifDiv = soup.find_all(class_="Gif")
        
        # grab img src from div
        for item in gifDiv:
            for img in item.find_all("img"):
                gifLinks.append(img["src"])
        
        if not gifLinks:
            await ctx.send("No GIFs found with given search critera.")
        else:
            await ctx.send(random.choice(gifLinks))
        
async def setup(bot):
    await bot.add_cog(Media(bot))