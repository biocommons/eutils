import lxml.etree

from eutils.exceptions import *
from eutils.xmlfacades.base import Base

class ESearchResults(Base):

    @property
    def count(self):
        return int( self._xmlroot.find('Count').text )

    @property
    def retmax(self):
        return int( self._xmlroot.find('RetMax').text )

    @property
    def retstart(self):
        return int( self._xmlroot.find('RetStart').text )

    @property
    def ids(self):
        return [ int(id) for id in self._xmlroot.xpath('/eSearchResult/IdList/Id/text()') ]

    @property
    def webenv(self):
        return self._xmlroot.find('WebEnv').text


    ############################################################################
    ## Internals
    @classmethod
    def _validate_xml(xml):
        """See Base.__init__ for explanation"""
        if '</eSearchResult>' not in xml:
            raise EutilsNCBIError("received malformed ESearchResult reply")
