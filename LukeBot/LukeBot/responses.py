import random
import media
import textGames

def get_response(message, user_message: str) -> str:
    p_message = user_message.lower()
    
    if p_message == "help": # Help
        return "Here are some useful '*' Commands:\n",
        "Hello: Hey There!\n",
        "RTD: Rolls a 6 sided die\n",
        "GIF YourTextHere: receive a random gif with your own prompt!"
    
    if p_message == "hello": # Hello
        return "Hey There!"
    
    if p_message == "rtd": # Roll The Dice
        return str(random.randint(1,6))

    if p_message[:4] == "gif ": # Receive a GIF
        return media.getGIF(p_message[4:])
    
    if p_message == "typerace":
        textGames.typeRace(message.channel, message.author)
    return "I don't understand what you said. Try typing \"help!\"." # Bad Input
