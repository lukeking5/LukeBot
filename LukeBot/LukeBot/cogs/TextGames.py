from calendar import c
import bot
import discord
from discord import app_commands
from discord.ext import commands
import random
import time
import asyncio
import os
import httpx
import json
from bs4 import BeautifulSoup
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageFilter
from io import BytesIO

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
            grid.close()
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
            word_site = "https://gist.githubusercontent.com/scholtes/94f3c0303ba6a7768b47583aff36654d/raw/d9cddf5e16140df9e14f19c2de76a0ef36fd2748/wordle-La.txt"
            response = httpx.get(word_site, timeout=.2) # this line fails without timeout ???
            WORDS = response.content.splitlines()
        except:
            await ctx.send("Word site failed to load")
            return

        idx = random.randint(0, len(WORDS) - 1)

        randWords = set() # will get answer word as well as 6 words in case user does not enter word within time limit

        
        while len(randWords) < 7:  # Keep looping until you have 7 words
            idx = random.randint(0, len(WORDS) - 1)
            word = WORDS[idx].decode("ascii")
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
                

    @commands.hybrid_command(name="picdle", description="Guess the animal!")
    async def picdle(self, ctx, difficulty):
        """Guess cat or dog. Easy, Med, or Hard"""
        # Image from URL into bytes to send in discord embed
        def urlToImgFile(response, embed, blur = None):

                image_data = BytesIO(response.content)
                image = Image.open(image_data)
                if blur != None:
                    image = image.filter(ImageFilter.BoxBlur(blur))
                image_data = BytesIO()  # Create a new BytesIO object for saving the image
                image.save(image_data, format='PNG')
                image_data.seek(0)
                fileImage = discord.File(image_data, filename="image.png")
                embed.set_image(url="attachment://image.png")
                return fileImage
        
        animalOptions = {0: "dog", 1: "cat"}
        difficulties = {"easy": 10, "med": 20, "hard": 40}
        update = None
        firstSend = True
        timeFlag = False
        try:
            selectedDifficulty = difficulties[difficulty.lower()]
        except:
            await ctx.send(f"Difficulty {difficulty} not valid.")
            return
        
        while(True):
            coinflip = random.randint(0,1)
            if coinflip == 0: # dog
                response = httpx.get("https://dog.ceo/api/breeds/image/random")
                image_url = response.json().get("message")
                response = httpx.get(image_url)
            elif coinflip == 1:
                response = httpx.get("https://cataas.com/cat")
            
            if response.status_code == 200:
                animal_embed = discord.Embed(title="Cat or Dog?", description="To guess, type 'cat' or 'dog'. 'end' will end the game.")
    
                fileImage = urlToImgFile(response, animal_embed, selectedDifficulty)
                
                if firstSend == True:
                    update = await ctx.send(embed=animal_embed, file=fileImage)
                    firstSend = False
                else:
                    await update.edit(embed=animal_embed, attachments=[fileImage])

                # reload image and make it unblurred. this does not update it yet, we will that later after user input
                fileImage = urlToImgFile(response, animal_embed)
                
            else:
                await ctx.send("Image not fetched")
                break
            
            # User guess
            try:
                user_guess = await self.bot.wait_for("message", timeout=30.0, check = lambda mess: mess.author == ctx.author and (mess.content == 'cat' or mess.content.lower() == 'dog'or mess.content.lower() == 'end'))
            except asyncio.TimeoutError: # if time out, show unblurred image and end game
                await ctx.send(f"Time limit for guess exceeded! Answer was: {animalOptions[coinflip]}")
                await update.edit(embed=animal_embed, attachments=[fileImage])
                return

            await update.edit(embed=animal_embed, attachments=[fileImage]) # update discord embed with unblurred image

            if str(user_guess.content).lower() == animalOptions[coinflip]: # user correct guess
                await update.add_reaction("✅")
                await asyncio.sleep(1)
                await update.remove_reaction(emoji="✅", member=self.bot.user)
            elif str(user_guess.content).lower() == 'end': # user ends game
                await ctx.send(f"Game ended. Answer was: {animalOptions[coinflip]}")
                return
            else: # user wrong guess
                await ctx.send(f"Wrong! Answer was: {animalOptions[coinflip]}. Game Over!")
                return

            
    @commands.hybrid_command(name="ttt", description="challenge another user to tic-tac-toe")
    async def ttt(self, ctx, user: discord.Member):
        """ Challenge another user to Tic-Tac-Toe"""
        def addTurn(firstStart, place=None, letter=None): # creates and fills grid based on list of user placement
            if firstStart == True:
                grid = Image.open('assets/tictactoe/grid.png') # create image background
            else:
                grid = Image.open('assets/tictactoe/gridNEW.png')
            match place:
                case 1:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (0,0))
                case 2:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (167,0))
                case 3:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (334,0))
                case 4:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (0,167))
                case 5:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (167,167))
                case 6:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (334,167))
                case 7:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (0,334))
                case 8:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (167,334))
                case 9:
                    grid.paste(Image.open(f'assets/tictactoe/{letter}.png'), (334,334))
                case _:
                    pass
            grid.save('assets/tictactoe/gridNEW.png')
            grid.close()
            return discord.File("assets/tictactoe/gridNEW.png")
        
        # discord user accept/deny challenge
        await ctx.send(f"{user.mention}: You have 10 seconds to accept or deny {ctx.author.mention}'s TIC-TAC-TOE challenge. 'accept' or 'deny'.")
        try:
            userAns = await self.bot.wait_for("message", check = lambda mess: mess.author == user and (mess.content.lower() == 'accept' or mess.content.lower() == 'deny'), timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send(f"Game cancelled. {user.mention} failed to respond.")
            return
        if userAns == 'deny':
            await ctx.send(f"{user.mention} denied TIC-TAC-TOE.")
            return
        await ctx.send(f"Game starting! {ctx.author.mention} has first move.")
        
        userPlaced = {
            1: None, 2: None, 3: None, 
            4: None, 5: None, 6: None, 
            7: None, 8: None, 9: None
            }
        
        winCombinations = [
          [1, 2, 3],
          [4, 5, 6],
          [7, 8, 9],
          [1, 5, 9],
          [3, 5, 7],
          [1, 4, 7],
          [2, 5, 8],
          [3, 6, 9]
        ]
        # set up initial embed
        ttt_embed = discord.Embed(title="TIC-TAC-TOE", description="Type desired grid number for your turn.")
        emptyGrid = addTurn(True) # pass no args except bool to create new empty grid
        ttt_embed.set_image(url='attachments://gridNEW.png')
        update = await ctx.send(embed=ttt_embed, file=emptyGrid)
        
        # flag for win con
        flag = False
        for i in range(9):
            userNum = None # for scope
            # user enters 1-9 to make their turn.
            try:
                if i % 2 == 0:
                    getMsg = await self.bot.wait_for("message", check = lambda mess: mess.author == ctx.author and (int(mess.content) < 10 and int(mess.content) > 0 and userPlaced[int(mess.content)] is None), timeout=15.0)
                    userNum = int(getMsg.content)
                    userPlaced[userNum] = 'x'
                else:
                    getMsg = await self.bot.wait_for("message", check = lambda mess: mess.author == user and (int(mess.content) < 10 and int(mess.content) > 0 and userPlaced[int(mess.content)] is None), timeout=15.0)
                    userNum = int(getMsg.content)
                    userPlaced[userNum] = 'o'
            except asyncio.TimeoutError:
                await ctx.send("User failed to respond in time. Game forfeited.")
                break
                
            # update grid
            gridFile = addTurn(False, userNum, userPlaced[userNum])
            await update.edit(embed=ttt_embed, attachments=[gridFile])
            
            # check for win
            if i > 3: # no need to check unless 3 x's minimum have been placed
                for win in winCombinations:
                    if userPlaced[win[0]] == 'x' and userPlaced[win[1]] == 'x' and userPlaced[win[2]] == 'x':
                        await ctx.send(f"TIC-TAC-TOE!: User {ctx.author.mention} has won!")
                        flag = True
                        break
                    elif userPlaced[win[0]] == 'o' and userPlaced[win[1]] == 'o' and userPlaced[win[2]] == 'o':
                        await ctx.send(f"TIC-TAC-TOE!: User {ctx.author.mention} has won!")
                        flag = True
                        break
                    
            # if win is true break
            if flag == True:
                break
        
        # if loop has passed and no win condition has been met, no winner (cat's game)
        if flag == False:
            await ctx.send("Cat's game!")
        
        # remove generated png file
        os.remove('assets/tictactoe/gridNEW.png')
            

            
                
                
        
        
        
    
    
async def setup(bot):
    await bot.add_cog(TextGames(bot))