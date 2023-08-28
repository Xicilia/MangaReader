import discord
from discord.ext import commands
from core.parsers import getMangaInfo
from core.manager import ReaderManager, Reader
from utils.discordutils import getEmbedFromImageUrl


class MangaNavView(discord.ui.View):
    @discord.ui.button(label="Следующая", style=discord.ButtonStyle.green, custom_id="NextButton")
    async def buttonCallback(self, interaction: discord.Interaction, button: discord.Button):
        #TODO: create navigation buttons
        await interaction.response.edit_message(content="123")
        await interaction.response.defer()
        #await interaction.response.send_message()
        #await interaction.response.send_message("clicked", view=MangaNavView())
        

class MangaCog(commands.Cog):
    
    def __init__(self, bot):
        
        self.bot = bot
        
        self.manager = ReaderManager()
        
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
    
    async def buttonCallback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content="123")
    
    async def sendMangaMessage(self, ctx: commands.Context, reader: Reader):
        
        #button = discord.Button()
        #button.style = discord.ButtonStyle.green
        #button.label = "Следующая"
        #button.custom_id = "Next"
        #button.callback = self.buttonCallback
        
        await ctx.send(reader.getPageDescription(), file= await reader.getPageEmbed(), view=MangaNavView())
        
    @commands.hybrid_command(name="читать", description="Начать чтение манги", with_app_command=True)
    @discord.app_commands.describe(manga="Ссылка на мангу из сайта newmanga.org (или название из ссылки)")
    @discord.app_commands.rename(manga="манга")
    async def mangaReadStartCommand(self, ctx: commands.Context, manga: str):
          
        reader = self.manager.addReader(ctx.channel.id, manga)      
        
        await self.sendMangaMessage(ctx, reader)
        
    @commands.hybrid_command(name="следующая", description="Следующая страница манги", with_app_command=True)
    async def mangaNextPageCommand(self, ctx: commands.Context):
        
        reader = self.manager.getReaderByChannel(ctx.channel.id)
        reader.next()
        
        if not reader:
            await ctx.reply("Нет запущенной манги.", ephemeral=True)
            return
        
        await self.sendMangaMessage(ctx, reader)
          
        
async def setup(bot: commands.Bot):
    
    await bot.add_cog(MangaCog(bot))