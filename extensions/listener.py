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

        # Establish connection to db
            
        # get data for table
            
        # create new thread
            
        # commit data to db
        

def setup(client):
    client.add_cog(listener(client))