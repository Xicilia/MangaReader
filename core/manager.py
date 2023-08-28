from core.reader import Reader
from typing import Optional

class ReaderManager:
    
    def __init__(self):
        
        self._readers: list[Reader] = []
    
    def addReader(self, channelId: int, mangaName: str) -> Reader:
        
        self.removeReaderByChannel(channelId)
        
        reader = Reader(channelId, mangaName)
        self._readers.append(reader)
        
        return reader
        
    def getReaderByChannel(self, channelId: int) -> Optional[Reader]:
        
        for reader in self._readers:
            
            if reader.channelId == channelId:
                
                return reader
            
        else:
            
            return None
        
    def removeReaderByChannel(self, channelId: int):
        
        for reader in self._readers:
            
            if reader.channelId == channelId:
                
                self._readers.remove(reader)
                break