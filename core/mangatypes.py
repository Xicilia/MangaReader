from dataclasses import dataclass

@dataclass
class MangaInfo:
    """
    Represents all useful information about manga.
    """
    
    titleRU: str
    titleEN: str
    type: str
    rating: float
    status: str
    description: str
    thumbnailUrl: str
    chaptersTotal: int
    
@dataclass
class BranchInfo:
    
    id: int
    
@dataclass
class ChapterInfo:
    
    id: int
    tom: int
    number: int
    pages: int
    
@dataclass
class SliceInfo:    
    
    format: str
    path: str
    
    width: int
    height: int    
    
@dataclass
class PageInfo:
    
    index: int
    slices: list[SliceInfo]
    
    
@dataclass
class ChapterPages:
    
    chapterId: int
    origin: str
    pages: list[PageInfo]
