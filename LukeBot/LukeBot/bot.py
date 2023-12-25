import discord
import responses


async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    
    except Exception as e:
        print(e)
        

def run_discord_bot():
    TOKEN = 'MTE4ODY5NjAwMjQ3NjEyNjI5MA.GF2pxU.dR0zV9oJhV56f9gnZ_Ze5geRphWWqQpSSrTKBs'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')
    

    @client.event # HANDLES USER MESSAGES
    async def on_message(message):
        if message.author == client.user: # prevents bot from responding to intself
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
                await send_message(message, user_message, is_private=False)
            
        
    client.run(TOKEN)