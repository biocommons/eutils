import lxml.etree as le

from eutils.xmlfacades.base import Base
from eutils.xmlfacades.entrezgenelocus import EntrezgeneLocus

class Entrezgene(Base):

    _root_tag = 'Entrezgene'

    def __unicode__(self):
        return "TODO"

    @property
    def description(self):
        return self._xmlroot.findtext('Entrezgene_gene/Gene-ref/Gene-ref_desc')

    @property
    def gene_id(self):
        return int(self._xmlroot.findtext('Entrezgene_track-info/Gene-track/Gene-track_geneid'))

    @property
    def hgnc(self):
        return self._xmlroot.findtext('Entrezgene_gene/Gene-ref/Gene-ref_locus')

    @property
    def maploc(self):
        return self._xmlroot.findtext('Entrezgene_gene/Gene-ref/Gene-ref_maploc')

    @property
    def locus(self):
        n = self._xmlroot.find('Entrezgene_locus')
        return None if n is None else EntrezgeneLocus(n)

    @property
    def summary(self):
        return self._xmlroot.findtext('Entrezgene_summary')

    @property
    def synonyms(self):
        return self._xmlroot.xpath('Entrezgene_gene/Gene-ref/Gene-ref_syn/Gene-ref_syn_E/text()')

    @property
    def type(self):
        return self._xmlroot.find('Entrezgene_type').get("value")

    @property
    def genus_species(self):
        return self._xmlroot.xpath('Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_taxname/text()')[0]

    @property
    def common_tax(self):
        return self._xmlroot.xpath('Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_common/text()')[0]

    @property
    def tax_id(self):
        return int(self._xmlroot.xpath('Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_db/Dbtag[Dbtag_db/text()="taxon"]/Dbtag_tag/Object-id/Object-id_id/text()')[0])



if __name__ == "__main__":
    import gzip
    import os
    import lxml.etree
    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    data_file = os.path.join(data_dir, 'entrezgeneset.xml.gz')
    doc = lxml.etree.parse(gzip.open(data_file))
    n = doc.findall('.//Entrezgene')[0]
    o = Entrezgene(n)

