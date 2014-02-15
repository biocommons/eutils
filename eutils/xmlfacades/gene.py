import lxml.etree as le

from eutils.exceptions import *
from eutils.utils import xml_get_text, xml_get_text_or_none
import eutils.xmlfacades.base

class Gene(eutils.xmlfacades.base.Base):

    def __unicode__(self):
        return '{type}({self.hgnc}; {self.description})'.format(type=type(self).__name__,self=self)

    @property
    def description(self):
        return xml_get_text_or_none(self._xmlroot,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_desc')

    @property
    def gene_id(self):
        return int(xml_get_text_or_none(self._xmlroot,'/Entrezgene-Set/Entrezgene/Entrezgene_track-info/Gene-track/Gene-track_geneid'))

    @property
    def hgnc(self):
        return xml_get_text_or_none(self._xmlroot,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus')

    @property
    def maploc(self):
        return xml_get_text_or_none(self._xmlroot,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_maploc')

    @property
    def references(self):
        return [ GeneCommentary(gc) for gc in self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary') ]

    @property
    def summary(self):
        return xml_get_text_or_none(self._xmlroot,'/Entrezgene-Set/Entrezgene/Entrezgene_summary')

    @property
    def synonyms(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_syn/Gene-ref_syn_E/text()')

    @property
    def type(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_type/@value')[0]

    @property
    def genus_species(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_taxname/text()')[0]

    @property
    def common_tax(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_common/text()')[0]

    @property
    def tax_id(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_source/BioSource/BioSource_org/Org-ref/Org-ref_db/Dbtag[Dbtag_db/text()="taxon"]/Dbtag_tag/Object-id/Object-id_id/text()')[0]


    ############################################################################
    ## Internals

    @classmethod
    def _validate_xml(xml):
        if ('<Entrezgene-Set>' not in xml or '</Entrezgene-Set>' not in xml):
            raise EutilsNCBIError("Gene XML doesn't contain <Entrezgene-Set>..</Entrezgene-Set>")

    def _gene_commentary_nodes(self):
        return self._xmlroot.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary')



class GeneCommentary(object):
    """This class  a rudimentary interface for using "Gene-commentary" XML
    nodes in NCBI efetch replies.

    We'reparticularly focused on two kinds of G-c nodes: the "reference",
    which is higher in the XML tree, and the "target", which is a
    descendant of the reference. These are denoted by gcr and gct in the
    xpath below.  We're also interested in the optional
    Gene-commentary_genomic-coords, which contains the positions of the
    target (product) on the genomic sequence.

    /Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords
                                                ^ gcr                                    ^ gct           ^ gcgc

    gcr children contain reference sequence info (accession, etc)
    gct children contain target sequence info
    gcgc contains the actual coordinates
    """

    def __init__(self,gc):
        assert gc.tag == 'Gene-commentary'
        self._n = gc

    def __unicode__(self):
        return '{type}(acv={self.acv},type={self.type})'.format(type=type(self).__name__,self=self)

    def __str__(self):
        return unicode(self).encode('utf-8')

    @property
    def heading(self):
        try:
            return self._n.find('Gene-commentary_heading').text
        except AttributeError:
            raise EutilsNCBIError("Gene commentary has no heading.")

    @property
    def label(self):
        try:
            return self._n.find('Gene-commentary_label').text
        except AttributeError:
            raise EutilsNCBIError("Gene commentary has no label.")

    @property
    def accession(self):
        try:
            return self._n.find('Gene-commentary_accession').text
        except AttributeError:
            raise EutilsNCBIError("Gene commentary has no accession.")

    @property
    def version(self):
        try:
            return self._n.find('Gene-commentary_version').text
        except AttributeError:
            raise EutilsNCBIError("Gene commentary has no version.")

    @property
    def type(self):
        try:
            return self._n.find('Gene-commentary_type').get('value')
        except AttributeError:
            raise EutilsNCBIError("Gene commentary has no type.")

    @property
    def acv(self):
        return self.accession + '.' + self.version

    @property
    def products(self):
        return [ GeneCommentary(gc) for gc in self._n.xpath('Gene-commentary_products/Gene-commentary') ]
        
    @property
    def genomic_coords(self):
        try:
            return GeneCommentaryGenomicCoords(self._n.xpath('Gene-commentary_genomic-coords')[0])
        except IndexError:
            raise EutilsError("genomic coords are not defined for {self.acv}".format(self=self))


class GeneCommentaryGenomicCoords(object):
    """This class  a rudimentary interface for using "Gene-commentary_genomic-coords" XML
    nodes in NCBI efetch replies.
    """

    def __init__(self,gcgc):
        assert gcgc.tag == 'Gene-commentary_genomic-coords'
        self._n = gcgc

    @property
    def strand(self):
        nastrand = self._n.find('.//Na-strand').get('value')
        return 1 if nastrand == 'plus' else -1 if nastrand == 'minus' else None
    
    @property
    def gi(self):
        return self._n.find('.//Seq-id_gi').text

    @property
    def intervals(self):
        # N.B. NCBI XML uses 0-based, closed; convert to 0-based, right-open
        return [ (int(n.find('.//Seq-interval_from').text),int(n.find('.//Seq-interval_to').text)+1) 
                 for n in self._n.findall('.//Seq-interval') ]

    @property
    def exons_se_i(self,transcript_order=False):
        """return exon [start_i,end_i) pairs in reference sequence order, or transcript order if requested"""
        rev = transcript_order and self.strand == -1
        return sorted(self.intervals, reverse=rev)

