import lxml.etree as le

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.genecommentary import GeneCommentary

class EntrezgeneLocus(Base):

    _root_tag = 'Entrezgene_locus'

    def __unicode__(self):
        return 'TODO'

    @property
    def references(self):
        return [GeneCommentary(gc) for gc in self._xmlroot.findall('Gene-commentary')]


if __name__ == "__main__":
    import gzip
    import os
    import lxml.etree
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    data_file = os.path.join(data_dir, 'entrezgeneset.xml.gz')
    doc = lxml.etree.parse(gzip.open(data_file))
    n = doc.findall('.//Entrezgene')[0]
    o = Entrezgene(n)

