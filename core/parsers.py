from typing import Optional, Any
from core.mangatypes import MangaInfo, BranchInfo, ChapterInfo, PageInfo, SliceInfo, ChapterPages
from utils.httprequests import getRequest

#dict where KEY - value from json answer and VALUE - readable adaptation
_normalValues = {
    "manhya": "маньхуа",
    "manhwa": "манхва",
    "manga": "манга",
    "completed": "закончен",
    "on_going": "выпускается",
    "oel": "OEL-манга"
}

_mangaUrlStart = "https://newmanga.org/p/"
_mangaApiUrlStart = "https://api.newmanga.org/v2/projects/"
_mangaThumbnailStart = "https://img.newmanga.org/Large/webp/"

_mangaBranchUrl = "https://api.newmanga.org/v3/branches/{BranchId}/chapters/all"
_mangaChapterUrl = "https://api.newmanga.org/v3/chapters/{ChapterId}/pages"
_mangaPageUrl = "https://storage.newmanga.org/origin_proxy/{Origin}/{ChapterId}/{PagePath}"

def _normalizeMangaUrl(mangaName: str) -> str:

    if mangaName.startswith(_mangaUrlStart):
        
        return mangaName.replace(_mangaUrlStart,_mangaApiUrlStart)
    
    else:
        
        return f"{_mangaApiUrlStart}{mangaName}"

def getMangaName(mangaUrl: str) -> str:
    
    if mangaUrl.startswith(_mangaUrlStart):
        
        return mangaUrl.replace(_mangaUrlStart,"")
    
    else:
        
        return mangaUrl

def getChapterPages(chapterId: int) -> ChapterPages:
    
    rawInfo = getRequest(_mangaChapterUrl.replace("{ChapterId}", str(chapterId)), "JSON")
    
    pages = []
    for rawPageInfo in rawInfo["pages"]:
        
        
        slices = []
        for rawSliceInfo in rawPageInfo["slices"]:
            
            sliceSize = rawSliceInfo["size"]
            
            slices.append(
                SliceInfo(rawSliceInfo["format"], rawSliceInfo["path"], sliceSize["width"], sliceSize["height"])
            )
        
        pages.append(
            PageInfo(rawPageInfo["index"], slices)
        )
        
    return ChapterPages(chapterId, rawInfo["origin"], pages)
    

def getMangaBranch(branchId: int) -> list[ChapterInfo]:
    
    rawInfo: dict = getRequest(_mangaBranchUrl.replace("{BranchId}", str(branchId)), "JSON")
    
    chapters = []
    for rawChapterInfo in rawInfo:
        chapters.append(
            ChapterInfo(
                rawChapterInfo["id"],
                rawChapterInfo["tom"],
                rawChapterInfo["number"],
                rawChapterInfo["pages"]
            )
        )
        
    return chapters

def getMangaBranchInfo(mangaName: str) -> BranchInfo:
    
    rawInfo: dict = getRequest( _normalizeMangaUrl(mangaName), "JSON")
    
    return BranchInfo(rawInfo["branches"][0]["id"])


def getMangaPageUrl(origin: str, chapterId: int, pagePath: str) -> str:

    return _mangaPageUrl.replace("{Origin}", origin).replace("{ChapterId}", str(chapterId)).replace("{PagePath}", pagePath)


def getMangaPage(origin: str, chapterId: int, pagePath: str) -> Optional[Any]:
    
    url = getMangaPageUrl(origin, chapterId, pagePath)
    
    imageBytes = getRequest(url, "BYTE", True)
    
    return imageBytes
        

def getMangaInfo(mangaName: str) -> Optional[MangaInfo]:
    """
    Gets all useful info about manga.
    
    :param mangaName: url or name of manga. url should be https://newmanga.org/p/{MANGANAME}. MANGANAME can be extracted and passed as argument.
    
    Returns: MangaInfo object if manga was found, else None.
    """
    #print(mangaName)
    rawInfo: dict = getRequest( _normalizeMangaUrl(mangaName), "JSON")
    
    if not rawInfo:
        
        return None

    return MangaInfo(
        rawInfo["title"]["ru"],
        rawInfo["title"]["en"],
        _normalValues[rawInfo["type"]],
        round(rawInfo["rating"], 2),
        _normalValues[rawInfo["status"]],
        rawInfo["description"],
        f"{_mangaThumbnailStart}{rawInfo['image']['name']}",   
        rawInfo["branches"][0]["chapters_total"] # using first branch for now
    )
    
    