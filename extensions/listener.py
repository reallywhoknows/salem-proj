import discord
from discord.ext import commands
from datetime import date

class listener(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author.bot == True:
            return
        
        if isinstance(message.channel,discord.DMChannel):
            await message.channel.send("ty")

def setup(client):
    client.add_cog(listener(client))