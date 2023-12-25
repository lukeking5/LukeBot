import bot

def typeRace(channel, user):
    channel.send(f"Please type '*r' to join race. {user.mention()} may begin the race by typing '*start'")
    userList = []
    while(True):
        @client.event
        if bot.user_message == '*r':
            if bot.user_message.author in userList and not user:
                channel.send(f"User {bot.user_message.author} removed from race.")
                userList.remove(bot.user_message.author)

            else:
                channel.send(f"User {bot.user_message.author} added to race.")
                userList.append(bot.user_message.author)
        if bot.user_message == "*start" and bot.user_message.author == user:
            break
        print(userList)
    return 0