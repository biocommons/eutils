import lxml.etree as le

from eutils.exceptions import *
from eutils.utils import xml_get_text, xml_get_text_or_none
import eutils.xmlfacades.base

class PubMedArticle(eutils.xmlfacades.base.Base):
    def __unicode__(self):
        return( '{pma.__class__.__name__}({pma.pmid}; {pma.jrnl}; {pma.title}; {pma.authors})'.format(
                pma = self) )


    @property
    def abstract(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Abstract/AbstractText')

    @property
    def authors(self):
        # N.B. Citations may have 0 authors. e.g., pmid:7550356
        def _Last_FI(au):
            return au.find('LastName').text + ' ' + au.find('Initials').text
        return [ _Last_FI(au) for au
                 in self._xmlroot.xpath('/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/AuthorList/Author') ]

    @property
    def doi(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')

    @property
    def issue(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Issue')

    @property
    def jrnl(self):
        return ( xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/ISOAbbreviation')
                 or xml_get_text_or_none(self._xmlroot,'/PubmedArticleSetPubmedArticle/MedlineCitation/Article/Journal/Title') )
        return j

    @property
    def mesh_headings(self):
        return self._xmlroot.xpath('/PubmedArticleSet/PubmedArticle/MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName/text()')

    @property
    def pages(self):
        return( xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Pagination/MedlinePgn') )

    @property
    def pii(self):
        return xml_get_text_or_none(self._xmlroot,'PubmedData/ArticleIdList/ArticleId[@IdType="pii"]')

    @property
    def pmc(self):
        pmc = xml_get_text_or_none(self._xmlroot,'PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]')
        return None if pmc is None else pmc[3:]

    @property
    def pmid(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/PMID')

    @property
    def title(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/ArticleTitle')

    @property
    def volume(self):
        return xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Volume')
    
    @property
    def year(self):
        return (
            xml_get_text_or_none(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
            or xml_get_text(self._xmlroot,'/PubmedArticleSet/PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')[0:4]
            )

    def as_dict(self):
        return {
            'pmid': self.pmid,
            'jrnl': self.jrnl,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'year': self.year,
            'authors': self.authors,
            'title': self.title,
            'mesh_headings': self.mesh_headings,
            'abstract': self.abstract,
            }


