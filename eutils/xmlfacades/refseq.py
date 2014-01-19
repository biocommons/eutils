import lxml.etree as le

class RefSeq(object):
    def __init__(self,xml):
        self._root = le.fromstring(xml)

    @property
    def acv(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_accession-version/text()')[0]

    @property
    def cds_start_end(self):
        n = self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key/text()="CDS"]')
        assert len(n) == 1, "expected exactly one CDS GBFeature_key node"
        s,e = _feature_se(n[0])
        return s,e

    @property
    def cds_start_end_i(self):
        s,e = self.cds_start_end
        return s-1,e

    @property
    def chr(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature['
                                'GBFeature_key/text()="source"]/GBFeature_quals'
                                '/GBQualifier[GBQualifier_name/text()='
                                '"chromosome"]/GBQualifier_value')[0].text

    @property
    def exons(self):
        exon_nodes = self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]')
        return [ (s-1,e) for s,e in [ _feature_se(n) for n in exon_nodes ] ]

    @property
    def exon_names(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]'
                                '/GBFeature_quals/GBQualifier[GBQualifier_name="number"]'
                                '/GBQualifier_value/text()')
    @property
    def gene(self):
        return [ str(e)
                 for e in list(set(self._root.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature'
                                                    '/GBFeature_quals/GBQualifier[GBQualifier_name/text()="gene"]'
                                                    '/GBQualifier_value/text()'))) ]
    hgnc = gene                 # alias for gene method

    @property
    def seq(self):
        return self._root.xpath('/GBSet/GBSeq/GBSeq_sequence')[0].text


def _feature_se(gbf):
    loc = gbf.find('GBFeature_location').text
    if 'join' in loc:
        raise EutilsError('discontiguous genbank feature')
    s,e = loc.split('..')
    return int(s),int(e)
