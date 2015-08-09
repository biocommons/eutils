from eutils.utils import xml_get_text, xml_get_text_or_none
import eutils.xmlfacades.base
import eutils.xmlfacades.medlinecitation


class PubmedArticle(eutils.xmlfacades.base.Base):

    _root_tag = 'PubmedArticle'

    def __unicode__(self):
        return ('{self.__class__.__name__}({self.pmid}; {self.jrnl}; {self.title}; {self.authors})'.format(pma=self))

    @property
    def abstract(self):
        return self._medline_citation.abstract

    @property
    def authors(self):
        return self._medline_citation.authors

    @property
    def issue(self):
        return self._medline_citation.issue

    @property
    def jrnl(self):
        return self._medline_citation.jrnl

    @property
    def mesh_headings(self):
        return self._medline_citation.mesh_headings

    @property
    def pages(self):
        return self._medline_citation.pages

    @property
    def pmid(self):
        return self._medline_citation.pmid

    @property
    def title(self):
        return self._medline_citation.title

    @property
    def volume(self):
        return self._medline_citation.volume

    @property
    def year(self):
        return self._medline_citation.year

    @property
    def doi(self):
        return xml_get_text_or_none(self._xml_elem, 'PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')

    @property
    def pii(self):
        return xml_get_text_or_none(self._xml_elem, 'PubmedData/ArticleIdList/ArticleId[@IdType="pii"]')

    @property
    def pmc(self):
        pmc = xml_get_text_or_none(self._xml_elem, 'PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]')
        return None if pmc is None else pmc[3:]

    @property
    def _medline_citation(self):
        return eutils.xmlfacades.medlinecitation.MedlineCitation(self._xml_elem.find('MedlineCitation'))


if __name__ == "__main__":
    from eutils.xmlfacades.pubmedarticleset import PubmedArticleSet
    import lxml.etree as le
    import os
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpaths = [
        'efetch.fcgi?db=pubmed&id=20412080&rettype=xml.xml', 'efetch.fcgi?db=pubmed&id=22351513&retmode=xml.xml',
        'efetch.fcgi?db=pubmed&id=23121403&retmode=xml.xml'
    ]
    path = os.path.join(data_dir, relpaths[0])
    pas = PubmedArticleSet(le.parse(path).getroot())
    pa = iter(pas).next()
