from .request import RequestHandler
from .common import CommonHandler


class DgAPI:
    
    def __init__(self, api_key: str = None):
        
        if api_key: pass 
            
        self.request = RequestHandler() 
        self.common = CommonHandler(self.request)
        
    def __repr__(self) -> str:
        pass
    
    def __str__(self) -> str:
        pass
