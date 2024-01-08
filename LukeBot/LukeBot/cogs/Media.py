import random
import time
import json
import httpx
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord import app_commands
from databases.databases import cmdToDB

class Media(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="gif", description="Receive a random gif based on the prompt.")
    async def gif(self, ctx, *, arg):
        """Receive a random gif based on the prompt"""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id), arg)
        
        arg = arg.replace(' ', '-') # spaces become %20 in image search. ############### LATER SHOULD IMPLEMENT MORE SUCH AS '+' ##############
        gifLinks = []
        
        # grab API key
        apiFile = open("C:/Users/schwa/Desktop/API_KEYS/TENOR.txt", "r")
        apiKey = apiFile.read()
        apiFile.close()
        
        # grabbing gifs
        response = httpx.get(f"https://tenor.googleapis.com/v2/search?q={arg}&key={apiKey}&limit={50}") #load first 500 gifs (timeout saved slow loading?)
        if response.status_code == 200:
            top100gifs = json.loads(response.content)
        else:
            top100gifs = None
            await ctx.send("Error retrieving GIFs")
            
        url = top100gifs['results'][random.randint(0, (len(top100gifs['results'])-1))]['url']
        
        await ctx.send(url)
 
    @commands.hybrid_command(name="wr", description="Retrieve information about LoL players or champions.")
    async def wr(self, ctx, *, arg):
        """Retrieve information about LoL players or champions."""
        cmdToDB(ctx.command.name, str(ctx.guild.id), str(ctx.author.id), arg)
        
        newArg = arg.replace(' ', '') #spaces on u.gg website are removed

        headers = { # spoofing browser to webscrape
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Referer': 'https://www.google.com/'
                }
        
        ### USER SEARCHES FOR PLAYER ###
        if '#' in newArg:
            newArg = newArg.replace('#', '-') # '#' changed to '-' in link
            response = httpx.get(f"https://u.gg/lol/profile/na1/{newArg}/overview", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            
            try: # grab player data
                rankImage = soup.find("img", class_="rank-img")
                rankImage = rankImage["src"]
                playerRank = soup.find(class_="rank-text").get_text(separator=' ', strip=True)
                playerWR = soup.find(class_="rank-wins") # keep this for playerGames
                playerWRText = playerWR.get_text(separator=' ', strip=True)
                playerGames = playerWR.find(class_="total-games") # subclass of playerWR
                playerChamps = soup.find_all(class_="champion-name") 
            except:
                await ctx.send("Player Not Found.")
                return
            
            playerChampsText = ""
            for i, champ in enumerate(playerChamps): # playerChamps is ResultSet of champion text, make one string for dictionary value
                if i != (len(playerChamps) - 1):
                    playerChampsText += (champ.text + ", ")
                else:
                    playerChampsText += champ.text

            playerInfo = {"Summoner Rank:": playerRank, "Summoner Winrate:": playerWRText, "Summoner Champions:": playerChampsText}

            # create embed for player
            player_embed = discord.Embed(title=arg.split("#", 1)[0].upper())
            for i, key in enumerate(playerInfo):
                if i == 2:
                    player_embed.add_field(name=key, value=playerInfo[key], inline=False)
                else:
                    player_embed.add_field(name=key, value=playerInfo[key])
            player_embed.set_thumbnail(url=rankImage)
            
            await ctx.send(embed=player_embed)
            
        ### USER SEARCHES FOR CHAMP ###
        else:
        #content of search URL
            response = httpx.get(f"https://u.gg/lol/champions/{newArg}/build", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            try: # grab champ data
                champImage = soup.find("img", class_="champion-image")
                champImage = champImage["src"]
                champStats = soup.find(class_="additional-stats-container") # container that holds champion stats
                values = champStats.find_all(class_="value") # values of champion stats
            except:
                await ctx.send("Champion Not Found.")
                return
        
            # create embed for champion
            champ_embed = discord.Embed(title=arg.upper(), description="Champion Statistics")
            champInfo = {"Tier": values[0].text, "Win Rate": values[1].text, "Pick Rate": values[2].text, "Ban Rate:": values[3].text, "Matches": values[4].text}
            for key in champInfo:
                champ_embed.add_field(name=key, value=champInfo[key])
            champ_embed.set_thumbnail(url=champImage)

            await ctx.send(embed=champ_embed)
        
async def setup(bot):
    await bot.add_cog(Media(bot))