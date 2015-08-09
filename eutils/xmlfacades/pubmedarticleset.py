import eutils.xmlfacades.base
from eutils.xmlfacades.pubmedarticle import PubmedArticle


class PubmedArticleSet(eutils.xmlfacades.base.Base):

    _root_tag = 'PubmedArticleSet'

    def __iter__(self):
        return (PubmedArticle(pa_n) for pa_n in self._xml_elem.iterfind('PubmedArticle'))


if __name__ == "__main__":
    import gzip
    import os
    import lxml.etree as le

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpaths = [
        'efetch.fcgi?db=pubmed&id=20412080&rettype=xml.xml', 'efetch.fcgi?db=pubmed&id=22351513&retmode=xml.xml',
        'efetch.fcgi?db=pubmed&id=23121403&retmode=xml.xml'
    ]

    pmasets = [PubmedArticleSet(le.parse(os.path.join(data_dir, relpath)).getroot()) for relpath in relpaths]
