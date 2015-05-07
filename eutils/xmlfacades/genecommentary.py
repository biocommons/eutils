from eutils.xmlfacades.base import Base
from eutils.xmlfacades.genecommentarygenomiccoords import GeneCommentaryGenomicCoords

class GeneCommentary(Base):
    """This class  a rudimentary interface for using "Gene-commentary" XML
    nodes in NCBI efetch replies.

    We're particularly focused on two kinds of G-c nodes: the
    "reference", which is higher in the XML tree, and the "product",
    which is a descendant of the reference.

    """

    _root_tag = 'Gene-commentary'

    def __unicode__(self):
        return "TODO"

    @property
    def type(self):
        return self._xmlroot.find('Gene-commentary_type').get("value")

    @property
    def heading(self):
        return self._xmlroot.findtext('Gene-commentary_heading')

    @property
    def label(self):
        return self._xmlroot.findtext('Gene-commentary_label')

    @property
    def accession(self):
        return self._xmlroot.findtext('Gene-commentary_accession')

    @property
    def version(self):
        return self._xmlroot.findtext('Gene-commentary_version')

    @property
    def acv(self):
        if self.accession is None or self.version is None:
            return None
        return self.accession + '.' + self.version

    @property
    def products(self):
        return [GeneCommentary(gc) for gc in self._xmlroot.xpath('Gene-commentary_products/Gene-commentary')]
        
    @property
    def genomic_coords(self):
        gcgcs = self._xmlroot.xpath('Gene-commentary_genomic-coords')
        if len(gcgcs) == 0:
            return None
        assert len(gcgcs) == 1
        return GeneCommentaryGenomicCoords(gcgcs[0])


