"""locus.ncbi.pubmed -- tools to deal with NCBI's E-utilities interface to PubMed"""

# This helps debug:
# curl 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id=19483685'

import grp, logging, os, pprint, sys
import xml.etree.ElementTree as ET

from Bio import Entrez

import locus
from locus.core.configwrapper import locusconfig
from locus.core.decorators.memoized import memoized
from locus.core.exceptions import *

logger = logging.getLogger()

Entrez.email = locusconfig.get('ncbi','email')
Entrez.tool =  locusconfig.get('ncbi','tool')

class PubMedArticle(object):
    def __init__(self,pmid=None):
        if pmid is None:
            raise RuntimeError('must provide a PubMed id')
        self.pmid = str(pmid)
        self.art = _fetch_article(self.pmid)
        if self.art is None:
            raise LocusError("Couldn't find PubMed info for pmid:"+pmid)

    @property
    def abstract(self):
        return( self._get('MedlineCitation/Article/Abstract/AbstractText') )

    @property
    # N.B. Citations may have 0 authors. e.g., pmid:7550356
    def authors(self):
        authors = [ _au_to_last_fm(au) for au in self.art.findall('MedlineCitation/Article/AuthorList/Author') ]
        return authors

    @property
    def authors_str(self):
        return( '; '.join(self.authors) )

    @property
    def author1_last_fm(self):
        """return first author's name, in format Last INITS (space between surname and inits)"""
        return _au_to_last_fm(self.art.find('MedlineCitation/Article/AuthorList/Author'))

    @property
    def author1_lastfm(self):
        """return first author's name, in format LastINITS"""
        if self.author1_last_fm is not None:
            return self.author1_last_fm.replace(' ','')
        return None

    @property
    def jrnl(self):
        j = self._get('MedlineCitation/Article/Journal/ISOAbbreviation')
        if j is None:
            # e.g., http://www.ncbi.nlm.nih.gov/pubmed?term=21242195
            j = self._get('MedlineCitation/Article/Journal/Title')
        assert j is not None
        return j

    @property
    def pages(self):
        return( self._get('MedlineCitation/Article/Pagination/MedlinePgn') )

    @property
    def first_page(self):
        try:
            return self.pages.partition('-')[0]
        except AttributeError:
            return None

    @property
    def title(self):
        return( self._get('MedlineCitation/Article/ArticleTitle') )

    @property
    def volume(self):
        try:
            return self.art.find('MedlineCitation/Article/Journal/JournalIssue/Volume').text
        except AttributeError:
            return None

    @property
    def issue(self):
        try:
            return self.art.find('MedlineCitation/Article/Journal/JournalIssue/Issue').text
        except AttributeError:
            return None

    @property
    def voliss(self):
        ji = self.art.find('MedlineCitation/Article/Journal/JournalIssue')
        try:
            return( '%s(%s)' % (ji.find('Volume').text,
                                ji.find('Issue').text) )
        except AttributeError:
            pass
        try:
            return( ji.find('Volume').text )
        except AttributeError:
            pass
        # electronic pubs may not have volume or issue
        # e.g., http://www.ncbi.nlm.nih.gov/pubmed?term=20860988
        logger.info("No volume for "+self.pmid)
        return None

    @property
    def year(self):
        y = self._get('MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
        if y is None:
            # case applicable for pmid:9887384 (at least)
            y = self._get('MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')[0:4]
        assert y is not None
        return y

    @property
    def doi(self):
        return self._get('PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')

    @property
    def pii(self):
        return self._get('PubmedData/ArticleIdList/ArticleId[@IdType="pii"]')

    @property
    def pmc(self):
        try:
            return self._get('PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]')[3:]
        except TypeError:
            return None

    ######################################################################
    ## INTERNAL CLASS FUNCTIONS
    def _get(self,tag):
        n = self.art.find(tag)
        if n is not None:
            return n.text
        return None
    
    def __str__(self):
        return( '%s (%s. %s, %s:%s)'.format(
            self.title, self.authors_str, self.jrnl, self.voliss, self.pages) )
        



############################################################################
## Utilities

#@memoized
def _fetch_article(pmid):
    # TODO: potential for race condition on write, but vanishingly unlikely
    cache_dir = locusconfig.get('locus','cache_dir')
    if not os.path.exists(cache_dir):
        gid = grp.getgrnam(locusconfig.get('locus','dir_group')).gr_gid
        os.makedirs(cache_dir)
        try:
            os.chown(cache_dir, -1, gid)    # -1 == don't change owner
        except OSError as e:
            logger.warn(cache_dir + ': ' + str(e))
            pass
        os.chmod(cache_dir,int(locusconfig.get('locus','dir_mode'),8))
    xml_fn = os.path.join(cache_dir,'ncbi-pubmed-%s.xml' % (pmid))
    if os.path.exists(xml_fn):
        logger.info('fetched '+pmid+' from debug cache')
        dom = ET.parse(xml_fn)
    else:
        xml = Entrez.efetch(db='pubmed', id=pmid, retmode='xml').read()
        dom = ET.fromstring(xml)
        logger.info('fetched PubMed '+pmid+' via NCBI E-Utilities')
        with open(xml_fn,'w') as fp:
            fp.write(xml)
            logger.info('wrote '+xml_fn)
    art = dom.find('PubmedArticle')
    return art

def _au_to_last_fm(au):
    if au is None:
        return
    try:
        return( au.find('LastName').text
                + u' ' + au.find('Initials').text )
    except AttributeError:
        pass
    try:
        return( au.find('CollectiveName').text )
    except AttributeError:
        pass
    try:
        return( au.find('LastName').text )
    except AttributeError:
        pass
    raise Exception("Author structure not recognized")

