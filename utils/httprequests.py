import requests

from typing import Optional, Any, Callable

def _serializeResponseToPlainText(response: requests.Response) -> str:
    """
    Gets answer's text
    """
    response.encoding = "utf-8"
    return response.text

def _serializeResponseToJson(response: requests.Response) -> Optional[dict]:
    """
    Gets answer's json, if any.
    """
    try:
        return response.json()
    except:

        return None

def _serializeResponseToByte(response: requests.Response) -> Any:
    
    return response.raw

def _getSerializer(type: str) -> Callable[[requests.Response], Any]:
    """
    Returns serializer depends on type.
    """
    if type == "TEXT":
        return _serializeResponseToPlainText
    elif type == "JSON":
        return _serializeResponseToJson
    elif type == "BYTE":
        return _serializeResponseToByte
    else:
        raise TypeError(type)

def getRequest(url: str, returningResponseType: str, stream: bool = False) -> Optional[Any]:
    
    response = requests.get(url, stream=stream)
    print(url)
    if response.status_code != 200:
        
        return None
    
    return _getSerializer(returningResponseType)(response)
    
    
    
