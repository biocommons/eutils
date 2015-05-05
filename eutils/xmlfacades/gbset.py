import lxml.etree

from eutils.exceptions import *
import eutils.xmlfacades.base

class GBSet(eutils.xmlfacades.base.Base):
    # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see client.py)

    def __unicode__(self):
        return "GBSet({self.acv})".format(self=self)


    @property
    def acv(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_accession-version/text()')[0]

    @property
    def cds(self):
        cds_f = self._cds_feature_node
        if cds_f is None:
            raise EutilsError("No CDS features defined for {self.acv}".format(self=self))
        return CDSFeature(cds_f)

    @property
    def comment(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_comment/text()')[0]

    @property
    def created(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_create-date/text()')[0]

    @property
    def definition(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_definition/text()')[0]

    @property
    def exons(self):
        return [ ExonFeature(n) for n in self._exon_feature_nodes ]

    @property
    def exons_se_i(self):
        return [ (e.start_i,e.end_i) for e in self.exons ]

    @property
    def cds_se_i(self):
        return (self.cds.start_i,self.cds.end_i)

    @property
    def genes(self):
        return [ str(e)
                 for e in list(set(self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature'
                                                    '/GBFeature_quals/GBQualifier[GBQualifier_name/text()="gene"]'
                                                    '/GBQualifier_value/text()'))) ]
    @property
    def gene(self):
        genes = self.genes
        if len(genes) > 1:
            raise EutilsError('{self.acv} is associated with {n} genes ({genes}); use genes (plural) property and select one yourself'.format(
                self=self,n=len(genes),genes=','.join(sorted(genes))))
        try:
            return genes[0]
        except IndexError:
            return None
        
    @property
    def gi(self):
        return int(self.seqids['gi'][0])              # always exactly one

    @property
    def length(self):
        return int(self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_length/text()')[0])

    @property
    def organism(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_organism/text()')[0]

    @property
    def seqids(self):
        """returns a dictionary of sequence ids, like {'gi': ['319655736'], 'ref': ['NM_000551.3']}"""
        seqids = self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_other-seqids/GBSeqid/text()')
        return dict( (t,l.rstrip('|').split('|'))
                     for t,_,l in [ si.partition('|') for si in seqids ] )

    @property
    def seq(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_sequence')[0].text.upper()
    sequence = seq

    @property
    def type(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_moltype/text()')[0]

    @property
    def updated(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_update-date/text()')[0]


    ############################################################################
    ## Internals

    @property
    def _cds_feature_node(self):
        cds_nodes = self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key/text()="CDS"]')
        if len(cds_nodes) > 1:
            raise EutilsError('More than 1 CDS feature for {self.acv}?!'.format(self=self))
        return None if len(cds_nodes) == 0 else cds_nodes[0]

    @property
    def _exon_feature_nodes(self):
        return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]')


class Feature(object):
    def __init__(self,feature_node):
        assert feature_node.tag == 'GBFeature'
        self._n = feature_node
        loc = self._n.find('GBFeature_location').text
        if 'join' not in loc:
            s,e = loc.split('..')
            self.start_i, self.end_i = int(s)-1,int(e)
            self.length = self.end_i - self.start_i

    # @property
    # def exon_names(self):
    #     return self._xmlroot.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]'
    #                             '/GBFeature_quals/GBQualifier[GBQualifier_name="number"]'
    #                             '/GBQualifier_value/text()')


class CDSFeature(Feature):
    @property
    def translation(self):
        return self._n.xpath('GBFeature_quals/GBQualifier[GBQualifier_name/text()="translation"]/GBQualifier_value/text()')[0]

class ExonFeature(Feature):
    @property
    def inference(self):
        return self._n.xpath('GBFeature_quals/GBQualifier[GBQualifier_name/text()="inference"]/GBQualifier_value/text()')[0].replace('alignment:','')
