from .. import Client, EutilsError, EutilsNCBIError, EutilsNotFoundError


class ClientX(Client):
    """
    *warning* This class is subject to rapid development and api changes.

    A subclass of eutils.client.Client that provides specific lookup functions.

    This functionality is in a separate class because the API is experimental.
    """

    def fetch_gene_by_hgnc(self, hgnc):
        query = f'human[orgn] AND {hgnc}[preferred symbol] AND "current only"[Filter]'
        esr = self.esearch(db="gene", term=query)
        if esr.count != 1:
            msg = f"Received {esr.count} search replies for gene {hgnc} (query: '{query}')"
            raise EutilsError(msg)
        gene = next(iter(self.efetch(db="gene", id=esr.ids[0])))
        if hgnc != gene.hgnc:
            msg = f"Queried for {hgnc}, got reply for gene {gene.hgnc}"
            raise EutilsError(msg)
        return gene

    def fetch_nuccore_by_ac(self, acv):
        query = acv
        db = "nuccore"
        esr = self.esearch(db=db, term=query)
        if esr.count > 1:
            msg = f"Received {esr.count} replies for {acv} in database {db}"
            raise EutilsError(msg)
        if esr.count == 0:
            msg = f"No results for {query} in database {db}"
            raise EutilsNotFoundError(msg)
        gbseq = next(iter(self.efetch(db=db, id=esr.ids[0])))
        if acv != gbseq.acv:
            msg = f"Queried for {acv}, got reply for {gbseq.acv}"
            raise EutilsNCBIError(msg)
        return gbseq

    fetch_gbseq_by_ac = fetch_nuccore_by_ac

    def fetch_snps_for_gene(self, hgnc, organism="human"):
        db = "snp"
        esr = self.esearch(db=db, term=f"{hgnc}[gene name] AND {organism}[organism]")
        if esr.count == 0:
            msg = f"No results for gene {hgnc} and organism {organism} in database {db}"
            raise EutilsNotFoundError(msg)
        return next(iter(self.efetch(db=db, id=",".join(map(str, esr.ids)))))


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
