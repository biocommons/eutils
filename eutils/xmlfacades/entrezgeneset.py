from eutils.xmlfacades.base import Base
from eutils.xmlfacades.entrezgene import Entrezgene


class EntrezgeneSet(Base):
    """Represents a set of genes as provided with an XML reply from an
    Entrez Gene query.

    This object supports iteration, like this:

    >> xml = gzip.open(os.path.join("entrezgeneset.xml.gz")).read()
    >> doc = lxml.etree.XML(xml)
    >> egs = EntrezgeneSet(doc)
    >> len(egs.entrezgenes)
    4

    """

    _root_tag = 'Entrezgene-Set'

    def __unicode__(self):
        return '{type} ({chillin} children)'.format(
            type=type(self).__name__, chillin=len(self._xml_elem.getchildren()))

    @property
    def entrezgenes(self):
        # TODO: use cache decorator rather than homebrew
        try:
            return self._entrezgenes
        except AttributeError:
            self._entrezgenes = [Entrezgene(n) for n in self._entrezgene_nodes()]
            return self._entrezgenes

    def _entrezgene_nodes(self):
        return self._xml_elem.iterfind('Entrezgene')

    def __iter__(self):
        return (eg for eg in self.entrezgenes)
