import discord
import responses
from cogs.CoreCommands import CoreCommands
from cogs.Media import Media
from cogs.TextGames import TextGames
from discord.ext import commands, tasks

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(message, user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)
        

def run_discord_bot():
    TOKEN = 'MTE4ODY5NjAwMjQ3NjEyNjI5MA.GF2pxU.dR0zV9oJhV56f9gnZ_Ze5geRphWWqQpSSrTKBs'
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="*", intents=intents, help_command=None, case_insensitive=True)
    
    
    @bot.event
    async def on_ready():
        await bot.add_cog(CoreCommands(bot))
        await bot.add_cog(TextGames(bot))
        await bot.add_cog(Media(bot))
        print(f'{bot.user} is now running!')
    
    '''@bot.event # HANDLES USER MESSAGES
    async def on_message(message):
        if message.author == bot.user: # prevents bot from responding to intself
            return
        
        if len(str(message.content)) < 1: # prevents bot from crashing when someone joins server (0 length message)
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        

        print(f'{username} said: "{user_message}" ({channel})')
        
        
        if user_message[0] == '*': # User message must begin with *
            user_message = user_message[1:]
            if user_message.lower() == "help": # help gives private commands
                await send_message(message, user_message, is_private=True)
            else:
                await send_message(message, user_message, is_private=False)'''
            
        
    bot.run(TOKEN)