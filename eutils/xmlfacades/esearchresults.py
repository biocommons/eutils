import lxml.etree

from eutils.exceptions import *
from eutils.xmlfacades.base import Base

# TODO: implement results iterator
# once these objects contain a reference to the client,
# we'll be able to iterate using the webenv history
# See here:
# http://www.ncbi.nlm.nih.gov/books/NBK25500/#chapter1.Demonstration_Programs
# for($retstart = 0; $retstart < $Count; $retstart += $retmax) {
#   my $efetch = "$utils/efetch.fcgi?" .
#                "rettype=$report&retmode=text&retstart=$retstart&retmax=$retmax&" .
#                "db=$db&query_key=$QueryKey&WebEnv=$WebEnv";


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
