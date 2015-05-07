from eutils.xmlfacades.base import Base
from eutils.xmlfacades.entrezgene import Entrezgene


class EntrezgeneSet(Base):

    _root_tag = 'Entrezgene-Set'

    def __unicode__(self):
        return '{type} ({chillin} children)'.format(
            type=type(self).__name__, chillin=len(self._xmlroot.getchildren()))

    @property
    def entrezgenes(self):
        try:
            return self._entrezgenes
        except AttributeError:
            self._entrezgenes = [Entrezgene(n) for n in self._entrezgene_nodes()]
            return self._entrezgenes

    def _entrezgene_nodes(self):
        return self._xmlroot.iterfind('Entrezgene')
