import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import asyncio

ENVFILENAME = "env_settings.env"
load_dotenv(ENVFILENAME)

class BotBase(commands.Bot):
    """
    commands.Bot with some logic to sync slash commands.
    """
    
    def __init__(self, prefix: str, intents: discord.Intents):
        super().__init__(prefix, intents=intents)

        #self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):

        testGuild = discord.Object(id=1085257920410812446)  
        self.tree.copy_global_to(guild=testGuild)


        await self.tree.sync() 
        print('synced succesfully')
    
    async def on_guild_join(self, guild):

        await self.tree.sync(guild=guild)

    

#intents for bot
intents = discord.Intents.default()
intents.message_content = True

bot = BotBase("!", intents)

async def loadCogs():
    
    #parsing cogs files
    for filename in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__name__)), "cogs")):
        
        if filename.endswith(".py"):
            
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
asyncio.run(loadCogs())
        
bot.run(os.getenv("TOKEN"))