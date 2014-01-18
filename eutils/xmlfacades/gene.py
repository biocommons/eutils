import lxml.etree as le

from eutils.exceptions import *
from eutils.utils import xml_get_text, xml_get_text_or_none

class Gene(object):
    def __init__(self,xml):
        if (xml is None or len(xml) == 0):
            raise NCBIError("Gene XML is empty")
        if ('<Entrezgene-Set>' not in xml or '</Entrezgene-Set>' not in xml):
            raise NCBIError("Gene XML doesn't contain <Entrezgene-Set>..</Entrezgene-Set>")
        self._xml = xml
        self._root = le.fromstring(self._xml)
        self._gene_commentaries_gcs = None

    @property
    def desc(self):
        return xml_get_text_or_none(self._root,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_desc')

    @property
    def gene(self):
        return xml_get_text_or_none(self._root,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus')
    hgnc = gene                 # alias for gene method

    @property
    def maploc(self):
        return xml_get_text_or_none(self._root,'/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_maploc')

    @property
    def summary(self):
        t = self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_summary/text()')
        return None if len(t) == 0 else t[0]

    @property
    def gene_commentaries_gcs(self):
        if self._gene_commentaries_gcs is None:
            self._gene_commentaries_gcs = [ GeneCommentaryGC(n) 
                                            for n in self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus'
                                                                      '/Gene-commentary/Gene-commentary_products'
                                                                      '/Gene-commentary/Gene-commentary_genomic-coords') ]
        return self._gene_commentaries_gcs



############################################################################
## below here needs werious thinking about refactoring
    def grch37p10_mapping(self):
        gc = self._grch37p10_gc()
        si = gc.find('Gene-commentary_seqs/Seq-loc/Seq-loc_int/Seq-interval')
        ac = gc.find('Gene-commentary_accession').text
        v = gc.find('Gene-commentary_version').text
        if not ac.startswith('NC_'):
            raise NCBIError('mapping data not aligned to a chromosome?!')
        return { 
            'chr': _NC_to_chr(ac),
            'accession': ac,
            'version': v,
            'ac': ac+'.'+v,
            # N.B. NCBI XML uses 0-based, closed; convert to 0-based, right-open
            'start_i': int(si.find('Seq-interval_from').text),
            'end_i': int(si.find('Seq-interval_to').text)+1,
            'strand': si.find('Seq-interval_strand/Na-strand').get('value'),
            'gi': int(si.find('Seq-interval_id/Seq-id/Seq-id_gi').text),
            }

    def grch37p10_products(self):
        return [ '%s.%s' % (gcp.find('Gene-commentary_accession').text,
                            gcp.find('Gene-commentary_version').text) 
                 for gcp in self._grch37p10_gc().xpath('Gene-commentary_products/Gene-commentary') ]

    def grch37p10_product_exons(self,acv):
        # N.B. NCBI XML uses 0-based, closed; convert to 0-based, right-open
        return [ (int(n.find('Seq-interval_from').text),int(n.find('Seq-interval_to').text)+1) 
                 for n in self._grch37p10_product_intervals(acv) ]

    def grch37p10_product_strand(self,acv):
        gc = self._grch37p10_product_gc(acv)
        n = self._grch37p10_product_intervals(acv)[0]
        return n.find('Seq-interval_strand/Na-strand').get('value')

    def grch37p10_product_seq_id(self,acv):
        gc = self._grch37p10_product_gc(acv)
        n = self._grch37p10_product_intervals(acv)[0]
        return n.find('Seq-interval_id/Seq-id/Seq-id_gi').text

    ######################################################################
    ## Internal functions
    # TODO: Expand to manipulate alignments to non-chromosomal reference
    # e.g., NM_000034.3, gene 226, aligns to an NG and HuRef, but not
    # to GRCh37. Should use gis for all alignment

    def _grch37p10_product_gc(self,acv):
        ac,v = acv.split('.')
        gc = self._grch37p10_gc()
        pred = ' and '.join(['Gene-commentary_accession/text()="{ac}"',
                             'Gene-commentary_version/text()="{v}"'])
        pred = pred.format(ac=ac, v=v)
        xpath = 'Gene-commentary_products/Gene-commentary[%s]' % (pred)
        nodes = gc.xpath(xpath)
        if len(nodes) != 1:
            raise NCBIError("Got %d Gene-commentary_products for %s"%(len(nodes),acv))
        return nodes[0]
        
    def _grch37p10_product_intervals(self,acv):
        """NCBI's XML is inconsistent and undocumented, which means that
        we have to resort to reverse engineering questions like why
        NM_000014.4 and NM_005634.2 have different structures for seq
        intervals.  I'm sure it means something..."""
        gc = self._grch37p10_product_gc(acv)
        ints = gc.findall('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_mix/Seq-loc-mix/Seq-loc/Seq-loc_int/Seq-interval')
        if len(ints) > 0:
            return ints
        ints = gc.findall('Gene-commentary_genomic-coords/Seq-loc/Seq-loc_int/Seq-interval')
        if len(ints) > 0:
            return ints
        raise NCBIError('No product intervals for '+acv)

    def _grch37p10_gc(self):
        gcgcs = self.gene_commentaries_gcs
        return self._gc(heading='Reference GRCh37.p10 Primary Assembly')

    def _gc(self,heading):
        xpath = '/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary[Gene-commentary_heading[text()="%s"]]' % (heading)
        try:
            return self._root.xpath(xpath)[0]
        except IndexError:
            raise NCBIError("Didn't find Gene-commentary_heading = %s (may be in a patch)"%(heading))



class GeneCommentaryGC(object):
    """This class provides a rudimentary interface for dealing with
    "Gene-commentary_products" that have genomic coords. That is, nodes at
    this xpath:

    /Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords
                                                ^ gcr                                    ^ gct           ^ gcgc
    gcr children contain reference sequence info
    gct children contain target sequence info
    gcgc contains the actual coordinates
                                                
    gcs = self._root.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords')
    """

    def __init__(self,gcgc):
        self._gcgc = gcgc
        self._ancestors = list( self._gcgc.iterancestors() )
        self._gct = self._ancestors[0]
        self._gcr = self._ancestors[2]

    @property
    def ref_heading(self):
        return _gc_heading(self._gcr)
    @property
    def ref_label(self):
        return _gc_label(self._gcr)
    @property
    def ref_accession(self):
        return _gc_accession(self._gcr)
    @property
    def ref_version(self):
        return _gc_version(self._gcr)
    @property
    def ref_acv(self):
        return _gc_acv(self._gcr)

    @property
    def target_heading(self):
        return _gc_heading(self._gct)
    @property
    def target_label(self):
        return _gc_label(self._gct)
    @property
    def target_accession(self):
        return _gc_accession(self._gct)
    @property
    def target_version(self):
        return _gc_version(self._gct)
    @property
    def target_acv(self):
        return _gc_acv(self._gct)

def _gc_heading(gc):
    return gc.find('Gene-commentary_heading').text
def _gc_label(gc):
    return gc.find('Gene-commentary_label').text
def _gc_accession(gc):
    return gc.find('Gene-commentary_accession').text
def _gc_version(gc):
    return gc.find('Gene-commentary_version').text
def _gc_acv(gc):
    return _gc_accession(gc) + '.' + _gc_version(gc)
