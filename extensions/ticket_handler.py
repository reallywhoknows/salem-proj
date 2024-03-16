import discord
from discord.ext import commands
from datetime import date
import asyncio
import sqlite3

class listener(commands.Cog):
    def __init__(self,client):
        self.client = client

    @staticmethod
    async def generate_ticket(user, connection, cursor, channel):
        #Template for ticket before associating an ID
        title = "ticket-"

        # Generate a new empty ticket entry to get a new ticket ID
        cursor.execute(f'''INSERT INTO tickets VALUES (NULL,"{user.id}",NULL)''')
        connection.commit()

        # Grab the new empty entry not yet associated with a thread ID
        res = cursor.execute(f'''SELECT * FROM tickets WHERE user_id="{user.id}" AND thread_id IS NULL''')
        res = res.fetchall()

        # Use rowid as a ticket number
        ticket_number = str(res[0][0])
        title = title + ticket_number
        thread = await channel.create_thread(name=title, content=f"**Dear <@328236370462113792>, <@{user.id}> has reported the following...**")

        # Update empty entry with newly generated ticket
        cursor.execute(f'''UPDATE tickets SET thread_id="{thread.id}" WHERE rowid="{ticket_number}"''')
        connection.commit()
        return thread
    
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

        # Generate table
        connection.execute('''CREATE TABLE IF NOT EXISTS tickets (rowid INTEGER PRIMARY KEY, user_id TEXT, thread_id TEXT)''')

        # Working variables
        guild = self.client.get_guild(1087515364017066135)
        channel = discord.utils.get(guild.channels, name="tickets")
        user = message.author
        open_ticket = None

        # Queries DB looking for if the user has ever made at ticket
        res = cursor.execute(f'''SELECT user_id FROM tickets WHERE user_id="{user.id}"''')

        # Creates ticket for first time ticket creators
        if res.fetchall() == []:
            open_ticket = await listener.generate_ticket(user, connection, cursor, channel)
        else:
            #Grabs any tickets by thread id if the user has created one before
            res = cursor.execute(f'''SELECT thread_id FROM tickets WHERE user_id="{user.id}"''')
            for r in res.fetchall():
                thread_id = int(r[0])
                thread = channel.get_thread(thread_id)
            
            # Checks if any of the tickets the user previously created are open
            if not thread.locked:
                open_ticket = thread
                
        # Creates new ticket if all other tickets are closed.
        if open_ticket == None:
            open_ticket = await listener.generate_ticket(user, connection, cursor, channel)

        # Content handler
        # Check if message is empty & if there are attachments
        if message.content == "":
            for i in message.attachments:
                await open_ticket.send(i.url)
                return

        # Sends message content and attachments if there are any
        await open_ticket.send(f"{message.content}")
        for i in message.attachments:
            await open_ticket.send(i.url)












        res = cursor.execute(f'''SELECT * FROM tickets WHERE user_id="{user.id}"''')
        print(res.fetchall())

        # Gather User variables

        # commit data to db
        connection.commit()
        cursor.close()
        connection.close()

def setup(client):
    client.add_cog(listener(client))