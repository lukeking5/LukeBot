import bot
from discord.ext import commands
import random
import time
import asyncio

class TextGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def typeRace(self, ctx): ############ TIME NOT IMPLEMENTED FULLY YET. BOT.WAIT_FOR() PREVENTS TIME FROM INCREMENTING, AS IT WAITS FOR USER INPUT ##################
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
                    await ctx.send(f"User {user_message.author} added to race.")
                    userSet.add(bot.user_message.author)
            
            if user_message_content == "cancel": # if typerace initiator types *cancel, race is canceled. return to end function
                await ctx.send("Race Cancelled.")
                return
                
            if user_message_content == "start" and user_message.author == ctx.author: # typerace initiator types *start, race begins
                break
        
        typingFile = open("assets/typing_prompts.txt", "r") #open prompt file
        typingPrompt = random.choice(typingFile.readlines()).rstrip("\n") # grab random prompt
        typingFile.close() # close file
        
        for i in range(3, 0, -1): #Countdown
            if i == 3:
                await ctx.send("Prompt in 3...")
            else:
                await ctx.send(str(i) + "...")
            time.sleep(1)
            
        await ctx.send(typingPrompt + str(len(typingPrompt)))
        
        init_time = time.time() # Used to track
        stopwatch = time.time()   # time passed in race
        userDict = dict() # will hold users and wpm once race is finished
        while(time.time() < init_time + 45 and len(userSet) != 0):
            
            user_message = await self.bot.wait_for("message")
            user_message_content = str(user_message.content)
            
            if user_message_content == "end": # end race early
                return
            
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
                   
async def setup(bot):
    await bot.add_cog(TextGames(bot))