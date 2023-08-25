from core.parsers import getMangaBranchInfo, getMangaBranch


class Reader:
    
    def __init__(self, channelId: int, mangaName: str) -> None:

    
        self.channelId = channelId
        
        self.mangaName = mangaName
        
        self.branch = getMangaBranch( getMangaBranchInfo(self.mangaName).id )

        
        self.position = ReaderPosition()
        
    #def setChapter()
        
class ReaderPosition:
    
    def __init__(self, chapter: int = 0, page: int = 0, pageSlice: int = 0) -> None:
        
        self.chapter = chapter
        
        self.page = page
        
        self.pageSlice = pageSlice