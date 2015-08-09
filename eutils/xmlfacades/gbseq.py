import eutils.xmlfacades.base


class GBSeq(eutils.xmlfacades.base.Base):

    _root_tag = 'GBSeq'

    def __unicode__(self):
        return "GBSeq({self.acv})".format(self=self)

    @property
    def acv(self):
        return self._xml_elem.findtext('GBSeq_accession-version')

    @property
    def cds(self):
        cds_f = self._cds_feature_node
        if cds_f is None:
            raise EutilsError("No CDS features defined for {self.acv}".format(self=self))
        return CDSFeature(cds_f)

    @property
    def comment(self):
        return self._xml_elem.findtext('GBSeq_comment')

    @property
    def created(self):
        return self._xml_elem.findtext('GBSeq_create-date')

    @property
    def definition(self):
        return self._xml_elem.findtext('GBSeq_definition')

    @property
    def exons(self):
        return [ExonFeature(n) for n in self._exon_feature_nodes]

    @property
    def genes(self):
        return [str(e)
                for e in list(set(self._xml_elem.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature'
                                                       '/GBFeature_quals/GBQualifier[GBQualifier_name/text()="gene"]'
                                                       '/GBQualifier_value/text()')))]

    @property
    def gi(self):
        gis = self.seqids['gi']
        assert 1 == len(gis), "expected exactly one gi in XML"
        return int(gis[0])

    @property
    def length(self):
        return int(self._xml_elem.findtext('GBSeq_length'))

    @property
    def locus(self):
        return self._xml_elem.findtext('GBSeq_locus')

    @property
    def moltype(self):
        return self._xml_elem.findtext('GBSeq_moltype')

    @property
    def organism(self):
        return self._xml_elem.findtext('GBSeq_organism')

    @property
    def seqids(self):
        """returns a dictionary of sequence ids, like {'gi': ['319655736'], 'ref': ['NM_000551.3']}"""
        seqids = self._xml_elem.xpath('/GBSet/GBSeq/GBSeq_other-seqids/GBSeqid/text()')
        return dict((t, l.rstrip('|').split('|')) for t, _, l in [si.partition('|') for si in seqids])

    @property
    def sequence(self):
        return self._xml_elem.findtext('GBSeq_sequence').upper()

    @property
    def updated(self):
        return self._xml_elem.findtext('GBSeq_update-date')

    ############################################################################
    # Internals

    @property
    def _cds_feature_node(self):
        cds_nodes = self._xml_elem.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key/text()="CDS"]')
        if len(cds_nodes) > 1:
            raise EutilsError('More than 1 CDS feature for {self.acv}?!'.format(self=self))
        return None if len(cds_nodes) == 0 else cds_nodes[0]

    @property
    def _exon_feature_nodes(self):
        return self._xml_elem.xpath('/GBSet/GBSeq/GBSeq_feature-table/GBFeature[GBFeature_key="exon"]')


class Feature(object):
    def __init__(self, feature_node):
        assert feature_node.tag == 'GBFeature'
        self._n = feature_node
        loc = self._n.find('GBFeature_location').text
        if 'join' not in loc:
            s, e = loc.split('..')
            self.start_i, self.end_i = int(s) - 1, int(e)
            self.length = self.end_i - self.start_i


class CDSFeature(Feature):
    @property
    def translation(self):
        return self._n.xpath(
            'GBFeature_quals/GBQualifier[GBQualifier_name/text()="translation"]/GBQualifier_value/text()')[0]


class ExonFeature(Feature):
    @property
    def inference(self):
        return self._n.xpath(
            'GBFeature_quals/GBQualifier[GBQualifier_name/text()="inference"]/GBQualifier_value/text()')[0].replace(
                'alignment:', '')


if __name__ == "__main__":
    import os
    import lxml.etree as le
    from eutils.xmlfacades.gbset import GBSet

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpath = 'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml'
    path = os.path.join(data_dir, relpath)
    gbset = GBSet(le.parse(path).getroot())
    gbseq = iter(gbset).next()
