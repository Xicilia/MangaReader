import discord

def getEmbedFromImageUrl(url: str) -> discord.Embed:
    
    embed = discord.Embed()
    embed.set_image(url=url)
    return embed