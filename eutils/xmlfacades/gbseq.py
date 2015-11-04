# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from eutils.xmlfacades.base import Base

logger = logging.getLogger(__name__)

class GBSeq(Base):

    _root_tag = 'GBSeq'

    def __str__(self):
        return "GBSeq({self.acv})".format(self=self)

    @property
    def acv(self):
        return self._xml_root.findtext('GBSeq_accession-version')

    @property
    def cds(self):
        cds = self.features.cds
        return (cds.start_i, cds.end_i)

    @property
    def comment(self):
        return self._xml_root.findtext('GBSeq_comment')

    @property
    def created(self):
        return self._xml_root.findtext('GBSeq_create-date')

    @property
    def definition(self):
        return self._xml_root.findtext('GBSeq_definition')

    @property
    def exons(self):
        return [(f.start_i, f.end_i) for f in self.features.exons]

    @property
    def features(self):
        return GBFeatureTable(self._xml_root.find('GBSeq_feature-table'))

    @property
    def gene(self):
        return self.features.gene.qualifiers['gene']
    
    @property
    def genes(self):
        raise RuntimeError("The genes property is obsolete; use gene instead")

    @property
    def gi(self):
        gis = self.seqids['gi']
        assert 1 == len(gis), "expected exactly one gi in XML"
        return int(gis[0])

    @property
    def length(self):
        return int(self._xml_root.findtext('GBSeq_length'))

    @property
    def locus(self):
        return self._xml_root.findtext('GBSeq_locus')

    @property
    def moltype(self):
        return self._xml_root.findtext('GBSeq_moltype')

    @property
    def organism(self):
        return self._xml_root.findtext('GBSeq_organism')

    @property
    def other_seqids(self):
        """returns a dictionary of sequence ids, like {'gi': ['319655736'], 'ref': ['NM_000551.3']}"""
        seqids = self._xml_root.xpath('GBSeq_other-seqids/GBSeqid/text()')
        return {t: l.rstrip('|').split('|')
                for t, _, l in [si.partition('|') for si in seqids]}

    @property
    def sequence(self):
        return self._xml_root.findtext('GBSeq_sequence').upper()

    @property
    def updated(self):
        return self._xml_root.findtext('GBSeq_update-date')



class GBFeatureTable(Base):

    """Represents a collection of features associated with a genbank
    sequence

    Genbank features have types, referred to by their (non-unique)
    "keys", such as "gene", "CDS", "misc_feature", etc.  All features
    have locations and typically have additional, type specific
    "qualifiers".  Access to feature information is provided though
    GBFeature instances or subclasses.

    Subclasses of GBFeature are used to access additional data for
    specific feature types, such as GBFeatureCDS and GBFeatureExon for
    CDS and exon features, respectively.

    The cardinality of each feature type (name) varies: exactly 1
    gene, optionally 1 CDS, 0 or more exons and misc_features, etc.

    GBFeatureTable provides an iterator over all features, and returns
    GBFeature instances.
    
    In addition, when selecting features for specific types, the
    features are instantiated as their type-specific subclasses. This
    is the preferred selection mechanism for these feature types.

    """

    _root_tag = 'GBSeq_feature-table'

    def __iter__(self):
        return (GBFeature(n) for n in self._xml_root.iterfind('GBFeature'))
        
    @property
    def cds(self):
        key = 'CDS'
        nodes = self._get_nodes_with_key(key)
        assert len(nodes) <= 1, "Node has {n=n} {key} features! (expected <= 1)".format(n=len(nodes), key=key)
        return None if len(nodes) == 0 else GBFeatureCDS(nodes[0])

    @property
    def exons(self):
        key = 'exon'
        nodes = self._get_nodes_with_key(key)
        return [GBFeatureExon(n) for n in nodes]

    @property
    def gene(self):
        key = 'gene'
        nodes = self._get_nodes_with_key(key)
        assert len(nodes) <= 1, "Node has {n=n} {key} features! (expected <= 1)".format(n=len(nodes), key=key)
        return None if len(nodes) == 0 else GBFeature(nodes[0])

    @property
    def source(self):
        key = 'source'
        nodes = self._get_nodes_with_key(key)
        assert len(nodes) == 1, "Got {n=n} {key} features! (expected exactly 1)".format(n=len(nodes), key=key)
        return GBFeature(nodes[0])

    def _get_nodes_with_key(self, key):
        nodes = self._xml_root.xpath('GBFeature[GBFeature_key/text()="{key}"]'.format(key=key))
        return nodes



class GBFeature(Base):

    _root_tag = 'GBFeature'

    def __init__(self, xml):
        super(GBFeature, self).__init__(xml)
        loc = self._xml_root.findtext('GBFeature_location')
        if '..' in loc:
            s, e = loc.split('..')
            s, e = int(s), int(e)
        else:
            s = e = int(loc)
        self.start_i, self.end_i = s - 1, e  # interbase

    @property
    def key(self):
        return self._xml_root.findtext('GBFeature_key')

    @property
    def qualifiers(self):
        return {q.findtext('GBQualifier_name'): q.findtext('GBQualifier_value')
                for q in self._xml_root.findall('GBFeature_quals/GBQualifier')}

class GBFeatureCDS(GBFeature):

    @property
    def translation(self):
        return self._n.xpath(
            'GBFeature_quals/GBQualifier[GBQualifier_name/text()="translation"]/GBQualifier_value/text()')[0]

class GBFeatureExon(GBFeature):

    @property
    def inference(self):
        return self._n.xpath(
            'GBFeature_quals/GBQualifier[GBQualifier_name/text()="inference"]/GBQualifier_value/text()')[0]


if __name__ == "__main__":
    import os
    import lxml.etree as le
    from eutils.xmlfacades.gbset import GBSet

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpath = 'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml'
    path = os.path.join(data_dir, relpath)
    gbset = GBSet(le.parse(path).getroot())
    gbseq = next(iter(gbset))


# <LICENSE>
# Copyright 2015 eutils Committers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied. See the License for the specific language governing
# permissions and limitations under the License.
# </LICENSE>
