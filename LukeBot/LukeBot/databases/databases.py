from calendar import c
import sqlite3
from datetime import datetime

# adds command call to database
def cmdToDB(cmd: str, server: str, user: str, context:str = None):
    conn = sqlite3.connect('databases/commands.db')
    c = conn.cursor()
    
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # only uncomment if table does not exist
    '''c.execute("""CREATE TABLE command_calls ( 
                command_name text,
                calling_server_id text,
                calling_user_id text,
                time_called text,
                command_context text
              )""")'''
    
    if context:
        context = context.lower()
        
    c.execute("INSERT INTO command_calls VALUES (?, ?, ?, ?, ?)", (cmd, server, user, formatted_time, context))
        
    conn.commit()
    conn.close()