import discord
from core.parsers import getMangaBranchInfo, getMangaBranch, getMangaInfo, getChapterPages, getMangaPage
from core.mangatypes import ChapterPages
from typing import Optional, Any
from PIL import Image
import io

class Reader:
    
    def __init__(self, channelId: int, mangaName: str) -> None:

    
        self.channelId = channelId
        
        self.mangaName = mangaName
        
        self.info = getMangaInfo(self.mangaName)
        
        self.branch = getMangaBranch( getMangaBranchInfo(self.mangaName).id )
        
        self.chapter: ChapterPages = None
        self.updateChapter(0)
        
        self.position = _getReader(self.chapter)(self)
    
    def updateChapter(self, chapterIndex: int):
        
        self.chapter = getChapterPages( self.branch[chapterIndex].id )
    
    def next(self):
        
        self.position.nextPage()
    
    def getPageDescription(self):
        
        return f"{self.info.titleRU.capitalize()}. {self.position.serializePositionToStr()}"
                
    async def getPageEmbed(self) -> Optional[Any]:
        
        with io.BytesIO() as output:
            
            self.position.getCurrentPageImage().save(output, format="PNG")
            
            output.seek(0)
            
            return discord.File(fp=output, filename=f"{self.chapter.chapterId}part.png")
            

def _getReader(chapter: ChapterPages):
    
    page = chapter.pages[0]
    slice = page.slices[0]
    
    if slice.height > 1500:
        return WebReaderPosition
    else:
        return ReaderPosition
        
class ReaderPosition:
    
    def __init__(self, reader: Reader, chapter: int = 0, page: int = 0, pageSlice: int = 0) -> None:
        
        self._reader = reader
        
        self.chapterIndex = chapter
        
        self.pageIndex = page
        
        self.pageSliceIndex = pageSlice
    
    def nextPage(self):
        
        page = self._reader.chapter.pages[self.pageIndex]
        
        self.pageSliceIndex += 1
        if self.pageSliceIndex == len(page.slices):
            self.pageIndex += 1
            self.pageSliceIndex = 0
            
        if self.pageIndex == len(self._reader.chapter.pages):
            self.chapterIndex += 1
            self.pageIndex = 0
            self._reader.updateChapter(self.chapterIndex)
        
    def getCurrentPage(self):
        return self._reader.chapter.pages[self.pageIndex]
    
    def getCurrentSlice(self):
        return self.getCurrentPage().slices[self.pageSliceIndex]
    
    def getCurrentPageImage(self):
        
        slice = self.getCurrentSlice()
        
        return Image.open(getMangaPage(self._reader.chapter.origin, self._reader.chapter.chapterId, slice.path))
         
    def serializePositionToStr(self) -> str:
        
        return f"Глава {self.chapterIndex + 1}. Страница {self.pageIndex + 1}/{len(self._reader.chapter.pages)} часть {self.pageSliceIndex}/{len(self.getCurrentPage().slices)}."
    
            
    def updateChapter(self):
        
        self.chapter += 1
        self.page = 0
        self.pageSlice = 0
        
class WebReaderPosition(ReaderPosition):
    
    _slicePartsCount = 3 #in fact 3
    
    def __init__(self, reader: Reader, chapter: int = 0, page: int = 0, pageSlice: int = 0) -> None:
        super().__init__(reader, chapter, page, pageSlice)
        
        self.pageSlicePart = 0
        
        self.partWidth = 0
        self.partHeight = 0
    
    def findPartSize(self):
        
        slice = self.getCurrentSlice()
        
        self.partWidth = slice.width
        self.partHeight = slice.height / 3
    
    def serializePositionToStr(self) -> str:

        return super().serializePositionToStr() + f" ({self.pageSlicePart + 1}/3)"
    
    def nextPage(self):
        
        self.pageSlicePart += 1
        if self.pageSlicePart == WebReaderPosition._slicePartsCount:
            super().nextPage()
            self.pageSlicePart = 0
            
    def getCurrentPageImage(self):
        
        image = super().getCurrentPageImage()
        
        if self.partWidth == 0 and self.partHeight == 0:
            
           self.findPartSize() 
        
        top = self.partHeight * self.pageSlicePart
        bottom = top + self.partHeight
        
        imageHeight = image.size[1]
        
        bottom =  imageHeight if bottom > imageHeight else bottom   
        return image.crop((
            0, self.partHeight * self.pageSlicePart, image.size[0], bottom
        ))