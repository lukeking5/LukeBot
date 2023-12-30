import bot
import discord
from discord import app_commands
from discord.ext import commands
import random
import time
import asyncio
import os
import requests
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class TextGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="typerace", description="Create a type racer lobby.")
    async def typeRace(self, ctx): ############ TIME NOT IMPLEMENTED FULLY YET. BOT.WAIT_FOR() PREVENTS TIME FROM INCREMENTING, AS IT WAITS FOR USER INPUT ##################
        """Create a TypeRacer lobby."""
        await ctx.send(f"Please type 'race' to join/leave race. {ctx.author.mention} may begin the race by typing 'start' or cancel by typing 'cancel'")
        userSet = {ctx.author} # set of users currently ready to race
        while(True):
            user_message = await self.bot.wait_for("message")
            user_message_content = str(user_message.content)
            
            if user_message_content == "race": # user types race
                if user_message.author in userSet and not ctx.author: # if user is not author and has already entered race, he now exits race.
                    await ctx.send(f"User {bot.user_message.author} removed from race.")
                    userSet.remove(user_message.author)

                elif user_message.author != ctx.author: # if user is not author and types race
                    await ctx.send(f"User {user_message.author.mention} added to race.")
                    userSet.add(user_message.author)
            
            if user_message_content == "cancel": # if typerace initiator types *cancel, race is canceled. return to end function
                await ctx.send("Race Cancelled.")
                return
                
            if user_message_content == "start" and user_message.author == ctx.author: # typerace initiator types *start, race begins
                break
        
        typingFile = open("assets/typing_prompts.txt", "r") #open prompt file
        typingPrompt = random.choice(typingFile.readlines()).rstrip("\n") # grab random prompt
        typingFile.close() # close file
        
        for i in range(5, 0, -1): #Countdown
            if i == 5:
                await ctx.send("Prompt in 5...")
            else:
                await ctx.send(str(i) + "...")
            time.sleep(1)
            
        await ctx.send(typingPrompt)
        
        init_time = time.time() # Time race started
        userDict = dict() # will hold users and wpm once race is finished
        
        while(time.time() < init_time + 45 and len(userSet) != 0):
            stopwatch = time.time()
            user_message = await self.bot.wait_for("message")
            user_message_content = str(user_message.content)
            
            if user_message_content == "end": # end race early
                await ctx.send(f"{user_message.author.mention} has ended the race early.")
                break
            
            if user_message_content == typingPrompt and user_message.author in userSet: # user types prompt correctly
                await ctx.send(f"{user_message.author.mention} has finished!")
                userDict[user_message.author] = ((len(typingPrompt)/5)/((time.time() - init_time)/60.0)) # user : wpm
                userSet.remove(user_message.author) # remove user from set
                
            elif user_message_content != typingPrompt and user_message.author in userSet: # user types prompt incorrectly
                await ctx.send(f"Wrong, {user_message.author.mention}, try again!")
            
            if (init_time + 45 - stopwatch < 11 and init_time + 45 - stopwatch > 9): # 10 second warning
                await ctx.send("10 seconds left...")
            

        await ctx.send("\nRace Over! Results:")
        time.sleep(1)
        
        for i, user in enumerate(userDict): # Placements
            await ctx.send(f"{i + 1}. {user.mention}: {int(userDict[user])} WPM")
        if len(userSet) != 0:
               for user in userSet:
                   await ctx.send(f"{user.mention} did not finish.")
                   
    @commands.hybrid_command(name="wordle",description="Create a wordle game.")
    async def wordle(self, ctx): 
        """Create a wordle game."""
        def createGrid(guesses=None, word=''): # creates and fills grid based on list of user guesses
            if guesses is None:
                guesses = []
                
            grid = Image.new('RGB', (500,600), color=(207, 207, 207)) # create image background
            textPlane = ImageDraw.Draw(grid) # plane for characters to be drawn on
            font = ImageFont.truetype("arial.ttf", 60)
            for i in range(len(guesses)): # six rows
                if guesses[i]: # if not empty
                    tempWord = word # keeps track of correctly guessed/yellow letters so that there cannot be more yellows than there are instanes of that char
                    for j, char in enumerate(guesses[i]): #green letters
                        if char == word[j]: # correct char = green
                            tempWord = tempWord.replace(char, '', 1)
                            grid.paste(Image.open('assets/wordle/GreenSquare.png'), (j*100, i*100))
                            textPlane.text((j*100 + 25, i*100 + 25), str(char).upper(), (0,0,0), font=font)
                    for j, char in enumerate(guesses[i]): #yellow letters
                        if char in tempWord and char != word[j]: # incorrect but in word = yellow
                            tempWord = tempWord.replace(char, '', 1)
                            grid.paste(Image.open('assets/wordle/YellowSquare.png'), (j*100, i*100))
                            textPlane.text((j*100 + 25, i*100 + 25), str(char).upper(), (0,0,0), font=font)
                        elif char in word and char != word[j] and char not in tempWord: #if green/yellow exhausted of that char, should be gray
                            grid.paste(Image.open('assets/wordle/ColorAbsent.png'), (j*100, i*100))
                            textPlane.text((j*100 + 25, i*100 + 25), str(char).upper(), (0,0,0), font=font)
                    for j, char in enumerate(guesses[i]):
                        if char not in word:    
                            grid.paste(Image.open('assets/wordle/ColorAbsent.png'), (j*100, i*100))
                            textPlane.text((j*100 + 25, i*100 + 25), str(char).upper(), (0,0,0), font=font)
                else: #if guess yet entered, keep gray background
                    pass
            grid.save('assets/wordle/grid.png')
            return discord.File("assets/wordle/grid.png")

        # Set up initial embed below
        wordle_embed = discord.Embed(title="WORDLE", description="Type any five-letter word to guess!")
        #wordle_embed.set_author(name=f"{self.bot.user.name}") # Later, add github URL
        #wordle_embed.set_thumbnail(url=f"{self.bot.user.avatar_url}")
        gridFile = createGrid() # create empty grid to start
        wordle_embed.set_image(url="attachment://grid.png")
        
        update = await ctx.send(embed=wordle_embed, file=gridFile) #store embed message to update embed later
        
        # load dict of words
        try: 
            word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
            response = requests.get(word_site, timeout=.2) # this line fails without timeout ???
            WORDS = response.content.splitlines()
        except:
            await ctx.send("Word site failed to load")
            return

        idx = random.randint(0, 9999)

        word = str(WORDS[idx])[2:-1]

        randWords = set() # will get answer word as well as 6 words in case user does not enter word within time limit

        
        while len(randWords) < 7:  # Keep looping until you have 7 words
            idx = random.randint(0, 9999)
            word = str(WORDS[idx])[2:-1]
            if len(word) == 5 and word not in randWords:
                randWords.add(word)
        

        ans_word = random.choice(list(randWords)) # 5-letter 'answer' word
        randWords.remove(ans_word) # remove answer from random words
        
        #print(ans_word) so i can always cheat if i want. mwuahahaha
        
        guessList = [] # list of guesses

        flagGuess = False # flag for correct user guess
        
        for i in range(1,7): # loop through six guesses
            flagTimeLimit = False # time limit flag
            
            try:
                user_guess = await self.bot.wait_for("message", timeout=120.0, check = lambda mess: mess.author == ctx.author and len(mess.content) == 5)
            except asyncio.TimeoutError:
                await ctx.send(f"Time limit for guess exceeded! Random word {list(randWords)[0]} guessed.")
                flagTimeLimit = True

            guess = str(user_guess.content).lower() # always should be lowercase
            if flagTimeLimit == False: # add user guess if user guesses in time
                guessList.append(guess)
            else:
                guessList.append(list(randWords)[0]) # if time limit exceeded, add from randWord
                randWords.remove(list(randWords)[0])
                
            gridFile = createGrid(guessList, ans_word)
            await update.edit(embed=wordle_embed, attachments=[gridFile]) # update embed (grid image has changed)
            if guess == ans_word: # WIN CASE
                await ctx.send(f"Congratulations! {ctx.author.mention} won wordle! The word was: {ans_word}. Guesses taken: {len(guessList)}")
                flagGuess = True
                break
            
        if flagGuess == False:
            await ctx.send(f"{ctx.author.mention} has failed wordle. The word was: {ans_word}")
        
        os.remove('assets/wordle/grid.png') # delete generated grid image
                
async def setup(bot):
    await bot.add_cog(TextGames(bot))