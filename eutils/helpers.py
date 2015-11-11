# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import lxml.etree as le

# These helpers return the XML reply, after sanity checking.  They raise
# exceptions if the reply is invalid.  Names and ids are expected to be
# unique and therefore functions that take these raise an exception if the
# reply contains more than one record.


def esearch_nuccore_by_ac(ac):
    # N.B. [accn] only works for currect accessions
    xml = es.read(db='nuccore', term='%s[accn]' % (ac))
    if '<ErrorList><PhraseNotFound>' in xml:
        # N.B. [accn] only works for currect accessions
        logging.debug(
            "'%s[accn]' not found; trying unqualified search for unqualified query to pick up obsolete accession" %
            (ac))
        xml = es.read(db='nuccore', term=ac)
    if '</eSearchResult>' not in xml:
        raise LocusNCBIError("received malformed reply from NCBI for db=nuccore, ac=" + ac)
    return xml


def efetch_nuccore_by_id(id):
    xml = ef.read(db='nuccore', id=id, retmode='xml', rettype='gb')
    if '</GBSet>' not in xml:
        raise LocusNCBIError("received malformed reply from NCBI for db=nuccore, id=" + id)
    return xml


def efetch_nuccore_by_ac(ac):
    esr = ESearchResultParser(esearch_nuccore_by_ac(ac))
    if esr.Count == 0:
        raise LocusNCBIError('{ac}: transcript not found'.format(ac=ac))
    if esr.Count > 1:
        raise LocusNCBIError("received %d replies for %s" % (esr.Count, ac))
    return efetch_nuccore_by_id(esr.IdList[0])


def esearch_gene_by_hgnc_name(name):
    query = 'human[orgn] AND {name}[symbol] AND {name}[titl] AND "current only"[Filter]'.format(name=name)
    xml = es.read(rettype='uilist', db='gene', term=query)
    if '</eSearchResult>' not in xml:
        raise LocusNCBIError("received malformed reply from NCBI for db=gene, query=" + query)
    return xml


def efetch_gene_by_id(id):
    xml = ef.read(db='gene', id=id)
    if '</Entrezgene-Set>' not in xml:
        raise LocusNCBIError("received malformed reply from NCBI db=gene, id=" + id)
    return xml


def efetch_gene_by_hgnc_name(name):
    esr = ESearchResultParser(esearch_gene_by_hgnc_name(name))
    if esr.Count == 0:
        return None
    for id in esr.IdList:
        xml = efetch_gene_by_id(id)
        doc = le.XML(xml)
        reply_hgnc = doc.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus/text()')[0]
        if reply_hgnc == name:
            return xml
        logging.debug('queried for gene %s, skipped reply for gene %s' % (name, reply_hgnc))
    raise LocusNCBIError("NCBI search returned %d replies for %s, and none were for this gene!" % (esr.Count, name))


def elink_nuccore_to_gene(id):
    xml = el.read(dbfrom='nuccore', db='gene', linkname='nuccore_gene', id=id)
    if '</eLinkResult>' not in xml:
        raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=nuccore, dbto=gene, id=" + id)
    return xml


def elink_gene_to_nuccore(id):
    xml = el.read(dbfrom='gene', db='nuccore', linkname='gene_nuccore', id=id)
    if '</eLinkResult>' not in xml:
        raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=gene, dbto=nuccore, id=" + id)
    return xml

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
