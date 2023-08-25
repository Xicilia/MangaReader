import discord
from discord.ext import commands
from core.parsers import getMangaInfo
from utils.discordutils import getEmbedFromImageUrl

class MangaCog(commands.Cog):
    
    def __init__(self, bot):
        
        self.bot = bot
        
    @commands.hybrid_command(name="инфо", description="Информация о манге", with_app_command=True)
    @discord.app_commands.describe(manga="Ссылка на мангу из сайта newmanga.org (или название из ссылки)")
    @discord.app_commands.rename(manga="манга")
    async def mangaInfoCommand(self, ctx: commands.Context, manga: str):
        
        info = getMangaInfo(manga)
        
        if not info:
            await ctx.reply("Не могу получить информацию. Возможно некорректное название манги или сайт недоступен.", ephemeral=True)
            return
        
        await ctx.reply(
            f"{info.type.capitalize()}: {info.titleRU} ({info.titleEN})\n\n" +
            f"{info.description}\n\n" +
            f"Пользовательский рейтинг: {info.rating}\n" +
            f"Количество глав: {info.chaptersTotal}\n" +
            f"Статус: {info.status}\n", embed=getEmbedFromImageUrl(info.thumbnailUrl)
        )
        
        
async def setup(bot: commands.Bot):
    
    await bot.add_cog(MangaCog(bot))