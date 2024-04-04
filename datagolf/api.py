from .request import CommonHandler, RequestHandler


class DgAPI:
    
    def __init__(self, api_key: str = None):
        
        if api_key: pass 
            
        self.request = RequestHandler() 
        self.common = CommonHandler(self.request)
