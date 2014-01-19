from eutils.eutilsclient import EutilsClient
from eutils.xmlfacades.einfo import EInfo, EInfoDB
from eutils.xmlfacades.esearchresults import ESearchResults

class Client(object):
    def __init__(self):
        self._ec = EutilsClient()

    def einfo(self,db=None):
        if db is None:
            return EInfo( self._ec.einfo() )
        return EInfoDB( self._ec.einfo({'db':db}) )
        
    def esearch(self,db,term):
        return ESearchResults( self._ec.esearch({'db':db,'term':term}) )
