from os.path import split,splittext 

class DublinCoreAdapter:
    def __init__(self,filename):
        self._filename = filename 
    
    @property
    def title(self):
        return splittext(split(self._filename)[-1])[0]
    
    @property
    def languages(self):
        return ('en',)
    
    def __getitem__(self,item):
        return getattr(self,item,'Unkown')
    
class DublinCoreInfo(object):
    def summary(self,dc_dict):
        print('Title: %s' % dc_dict['title'])
        print('Creator: %s' % dc_dict['creator'])
        print('Languages: %s' % ', '.join(dc_dict['languages']))

