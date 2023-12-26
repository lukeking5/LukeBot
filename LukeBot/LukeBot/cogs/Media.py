import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from discord.ext import commands

random.seed(time.time())

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def gif(self, ctx, *, arg): # Function for grabbing random gif given string
        arg = arg.replace(' ', '-') # spaces become %20 in image search. ############### LATER SHOULD IMPLEMENT MORE SUCH AS '+' ##############
    
        driver = webdriver.Chrome()
        driver.get("https://tenor.com/search/" + arg + "-gifs") # tenor page based on input
        time.sleep(1.5) # wait to ensure all gifs load
        links = [f"{img.get_attribute('src')}" for img in driver.find_elements(By.XPATH, "//div[@class='Gif']//img[@src]")] # grabs all gif links on first page of imgur search
        driver.quit()
        await ctx.send(random.choice(links))

async def setup(bot):
    await bot.add_cog(Media(bot))