import discord
from discord.ext import commands
from datetime import date
import asyncio
import sqlite3

class listener(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        #Check if user is bot
        if message.author.bot == True:
            return
        
        #Check if message is a DM
        if isinstance(message.channel,discord.DMChannel):
            await message.channel.send("Thank you for your report, a ticket will be generated momentarily. Please refer back to the Salem discord.")

        # Establish connection to db
        connection = sqlite3.connect("db//tickets.db")
        cursor = connection.cursor()
        
        #       tickets
        # --------------------- 
        # | user_id |thread_id |
        # ---------------------

        connection.execute('''CREATE TABLE IF NOT EXISTS tickets (user_id TEXT, thread_id TEXT)''')

        # Working guild
        guild = self.client.get_guild(1087515364017066135)
        channel = discord.utils.get(guild.channels, name="report")
        user = message.author
        title = f"{message.author.name}'s report"
        open_ticket = None

        # Queries DB looking for if the user has ever made at ticket
        res = cursor.execute(f'''SELECT user_id FROM tickets WHERE user_id="{user.id}"''')

        # Creates entry for first time ticket-submitters
        if res.fetchall() == []:
            thread = await channel.create_thread(name=title, content="test")
            cursor.execute(f'''INSERT INTO tickets VALUES ("{user.id}","{thread.id}")''')

        # Grabs any tickets by thread id if the user has created one before
        res = cursor.execute(f'''SELECT thread_id FROM tickets WHERE user_id="{user.id}"''')
        for r in res.fetchall():
            thread_id = int(r[0])
            thread = channel.get_thread(thread_id)
            
            # Checks if any of the tickets the user previously created are open
            if not thread.locked:
                open_ticket = thread
                
        # Creates new ticket if all other tickets are closed.
        if open_ticket == None:
            print("All locked")

















        res = cursor.execute(f'''SELECT * FROM tickets WHERE user_id="{user.id}"''')
        print(res.fetchall())
        # Gather User variables

        # commit data to db
        connection.commit()
        cursor.close()
        connection.close()

def setup(client):
    client.add_cog(listener(client))