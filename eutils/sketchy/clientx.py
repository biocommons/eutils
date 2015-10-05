# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import eutils.client
from eutils.exceptions import EutilsError, EutilsNCBIError, EutilsNotFoundError


class ClientX(eutils.client.Client):
    """
    *warning* This class is subject to rapid development and api changes.

    A subclass of eutils.client.Client that provides specific lookup functions.

    This functionality is in a separate class because the API is experimental.
    """

    def fetch_gene_by_hgnc(self, hgnc):
        query = 'human[orgn] AND {hgnc}[preferred symbol] AND "current only"[Filter]'.format(hgnc=hgnc)
        esr = self.esearch(db='gene', term=query)
        if esr.count != 1:
            raise EutilsError("Received {n} search replies for gene {hgnc} (query: '{query}')".format(
                n=esr.count,
                hgnc=hgnc,
                query=query))
        gene = next(iter(self.efetch(db='gene', id=esr.ids[0])))
        if hgnc != gene.hgnc:
            raise EutilsError("Queried for {q_hgnc}, got reply for gene {r_hgnc}".format(q_hgnc=hgnc, r_hgnc=gene.hgnc))
        return gene

    def fetch_nuccore_by_ac(self, acv):
        query = acv
        db = 'nuccore'
        esr = self.esearch(db=db, term=query)
        if esr.count > 1:
            raise EutilsError("Received {n} replies for {acv} in database {db}".format(n=esr.count, acv=acv, db=db))
        if esr.count == 0:
            raise EutilsNotFoundError("No results for {query} in database {db}".format(query=query, db=db))
        gbseq = next(iter(self.efetch(db=db, id=esr.ids[0])))
        if acv != gbseq.acv:
            raise EutilsNCBIError("Queried for {q_acv}, got reply for {r_acv}".format(q_acv=acv, r_acv=gbseq.acv))
        return gbseq

    fetch_gbseq_by_ac = fetch_nuccore_by_ac

    def fetch_snps_for_gene(self, hgnc, organism='human'):
        db = 'snp'
        esr = self.esearch(db=db, term='%s[gene name] AND %s[organism]' % (hgnc, organism))
        if esr.count == 0:
            raise EutilsNotFoundError("No results for gene {hgnc} and organism {o} in database {db}".format(
                hgnc=hgnc,
                o=organism,
                db=db))
        return next(iter(self.efetch(db=db, id=','.join(map(str, esr.ids)))))


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
