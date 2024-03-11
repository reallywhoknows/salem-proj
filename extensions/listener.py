import discord
from discord.ext import commands
from datetime import date
import random
import asyncio
import hashlib
from hashlib import md5

class listener(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot == True:
            return
        
        if isinstance(message.channel,discord.DMChannel):
            await message.channel.send("Thank you for your report, a ticket will be generated momentarily. Please refer back to the Salem discord.")

            #Grab guild & category for channel creation
            guild = self.client.get_guild(329648419729571852)
            category_name = "Report"
            category = discord.utils.get(guild.categories, name=category_name)
            
            #Convert user to md5 in order to generate a unique (but reusable) ticket ID
            user = str(message.author)
            hash = hashlib.md5(user.encode()).hexdigest()[:8]

            #Generate ticket id and get channel
            ticket_id = f"ticket-{hash}"
            ticket_channel = discord.utils.get(guild.channels, name=ticket_id)

            #Create channel if it doesn't already exist and hyperlink reporting user
            if ticket_channel == None:
                await guild.create_text_channel(ticket_id, category=category)
                await asyncio.sleep(2)
                ticket_channel = discord.utils.get(guild.channels, name=ticket_id)
                await ticket_channel.set_permissions(message.author, read_messages=True, send_messages=True)
                await ticket_channel.send(f"**Dear <@328236370462113792>, <@{message.author.id}> has reported the following...**")

            #Forward DM content to private channel for review
            if message.content == "":
                for i in message.attachments:
                    await ticket_channel.send(i.url)
                    return
                
            await ticket_channel.send(f"{message.content}")
            for i in message.attachments:
                await ticket_channel.send(i.url)

def setup(client):
    client.add_cog(listener(client))