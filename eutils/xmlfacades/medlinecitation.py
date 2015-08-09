from eutils.utils import xml_get_text, xml_get_text_or_none
import eutils.xmlfacades.base

class MedlineCitation(eutils.xmlfacades.base.Base):

    _root_tag = 'MedlineCitation'

    @property
    def abstract(self):
        return self._xml_elem.findtext('Article/Abstract/AbstractText')

    @property
    def authors(self):
        # N.B. Citations may have 0 authors. e.g., pmid:7550356
        # Citations may also have a 'CollectiveName' author instead of one with a forename, lastname, and initials
        def _format_author(au):
            if au.find('CollectiveName') is not None:
                return au.find('CollectiveName').text
            elif au.find('LastName') is not None and au.find('Initials') is not None:
                return au.find('LastName').text + ' ' + au.find('Initials').text
            else:
                return au.find('LastName').text
        return [ _format_author(au) for au
                 in self._xml_elem.xpath('Article/AuthorList/Author') ]

    @property
    def issue(self):
        return self._xml_elem.findtext('Article/Journal/JournalIssue/Issue')

    @property
    def jrnl(self):
        return self._xml_elem.findtext('Article/Journal/ISOAbbreviation') or self._xml_elem.findtext('Article/Journal/Title')

    @property
    def mesh_headings(self):
        return self._xml_elem.xpath('MeshHeadingList/MeshHeading/DescriptorName/text()')

    @property
    def pages(self):
        return self._xml_elem.findtext('Article/Pagination/MedlinePgn')

    @property
    def pmid(self):
        return self._xml_elem.findtext('PMID')

    @property
    def title(self):
        return self._xml_elem.findtext('Article/ArticleTitle')

    @property
    def volume(self):
        return self._xml_elem.findtext('Article/Journal/JournalIssue/Volume')
    
    @property
    def year(self):
        return self._xml_elem.findtext('Article/Journal/JournalIssue/PubDate/Year') \
          or self._xml_elem.findtext('Article/Journal/JournalIssue/PubDate/Year') \
          or self._xml_elem.findtext('Article/Journal/JournalIssue/PubDate/MedlineDate')


if __name__ == "__main__":
    import lxml.etree as le
    import os

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    path = os.path.join(data_dir, 'medlinecitation-id=20412080.xml.gz')

    mc = MedlineCitation(le.parse(path).getroot())
