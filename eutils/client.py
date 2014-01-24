from eutils.exceptions import *
from eutils.queryservice import QueryService
from eutils.xmlfacades.einfo import EInfo, EInfoDB
from eutils.xmlfacades.esearchresults import ESearchResults
from eutils.xmlfacades.gene import Gene
from eutils.xmlfacades.pubmed import PubMedArticle
from eutils.xmlfacades.gbset import GBSet


class Client(object):

    def __init__(self):
        self._qs = QueryService()
        self.databases = self.einfo().databases


    def einfo(self,db=None):
        """query the einfo endpoint

        :param db: string (optional)
        :rtype: EInfo or EInfoDB object

        If db is None, the reply is a list of databases, which is returned
        in an EInfo object (which has a databases() method).

        If db is not None, the reply is information about the specified
        database, which is returned in an EInfoDB object.  (Version 2.0
        data is automatically requested.)
        """

        if db is None:
            return EInfo( self._qs.einfo() )
        return EInfoDB( self._qs.einfo({'db':db, 'version':'2.0'}) )
        

    def esearch(self,db,term):
        """query the esearch endpoint
        """
        return ESearchResults( self._qs.esearch({'db':db,'term':term}) )


    def efetch(self,db,id):
        """query the efetch endpoint
        """
        xml = self._qs.efetch({'db':db,'id':str(id)})
        if db in ['gene']:
            return Gene(xml)
        if db in ['nuccore']:
            # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see gbset.py)
            return GBSet(xml)
        if db in ['pubmed']:
            return PubMedArticle(xml)
        raise EutilsError('database {db} is not currently supported by eutils'.format(db=db))



    ############################################################################
    ## specific helpers

    def fetch_gene_by_hgnc(self,hgnc):
        query = 'human[orgn] AND {hgnc}[preferred symbol] AND "current only"[Filter]'.format(hgnc=hgnc)
        esr = self.esearch(db='gene',term=query)
        if esr.count != 1:
            raise EutilsError("Received {n} search replies for gene {hgnc} (query: '{query}')".format(
                n=esr.count, hgnc=hgnc, query=query))
        gene = self.efetch(db='gene',id=esr.ids[0])
        if hgnc != gene.hgnc:
            raise EutilsError("Queried for {q_hgnc}, got reply for gene {r_hgnc}".format(
                q_hgnc=hgnc, r_hgnc=gene.hgnc))
        return gene

    def fetch_nuccore_by_ac(self,acv):
        query = acv
        db = 'nuccore'
        esr = self.esearch(db=db,term=query)
        if esr.count > 1:
            raise EutilsError("Received {n} replies for {acv} in database {db}".format(
                n=esr.count, acv=acv, db=db))
        if esr.count == 0:
            raise EutilsNotFoundError("No results for {query} in database {db}".format(
                query=query, db=db))
        gbseq = self.efetch(db=db,id=esr.ids[0])
        if acv != gbseq.acv:
            raise EutilsNCBIError("Queried for {q_acv}, got reply for {r_acv}".format(
                q_acv=acv, r_acv=gbseq.acv))
        return gbseq

    fetch_gbseq_by_ac = fetch_nuccore_by_ac


    ## ############################################################################
    ## ## graveyard
    ## 
    ## def esearch_nuccore_by_ac(self,ac):
    ##     # N.B. [accn] only works for current accessions
    ##     xml = self.esearch(db='nuccore',term='%s[accn]' % (ac))
    ##     if '<ErrorList><PhraseNotFound>' in xml:
    ##         logging.debug("'%s[accn]' not found; trying unqualified search for unqualified query to pick up obsolete accession" % (ac))
    ##         xml = self.esearch(db='nuccore',term=ac)
    ##     return ESearchResults(xml)
    ## 
    ## def efetch_nuccore_by_id(self,id):
    ##     xml = ef.read(db='nuccore',id=id,retmode='xml',rettype='gb')
    ##     if '</GBSet>' not in xml:
    ##         raise LocusNCBIError("received malformed reply from NCBI for db=nuccore, id="+id)
    ##     return xml
    ## 
    ## def efetch_nuccore_by_ac(self,ac):
    ##     esr = ESearchResultParser( esearch_nuccore_by_ac(ac) )
    ##     if esr.Count == 0:
    ##         raise LocusNCBIError('{ac}: transcript not found'.format(ac=ac))
    ##     if esr.Count > 1:
    ##         raise LocusNCBIError("received %d replies for %s" % (esr.Count,ac))
    ##     return efetch_nuccore_by_id( esr.IdList[0] )
    ## 
    ## def efetch_gene_by_id(self,id):
    ##     xml = ef.read(db='gene',id=id)
    ##     if '</Entrezgene-Set>' not in xml:
    ##         raise LocusNCBIError("received malformed reply from NCBI db=gene, id="+id)
    ##     return xml
    ## 
    ## def efetch_gene_by_hgnc_name(self,name):
    ##     esr = ESearchResultParser( esearch_gene_by_hgnc_name(name) )
    ##     if esr.Count == 0:
    ##         return None
    ##     for id in esr.IdList:
    ##         xml = efetch_gene_by_id( id )
    ##         doc = le.XML(xml)
    ##         reply_hgnc = doc.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus/text()')[0]
    ##         if reply_hgnc == name:
    ##             return xml
    ##         logging.debug('queried for gene %s, skipped reply for gene %s' % (name,reply_hgnc))
    ##     raise LocusNCBIError("NCBI search returned %d replies for %s, and none were for this gene!" % (
    ##             esr.Count, name))
    ## 
    ## def elink_nuccore_to_gene(self,id):
    ##     xml = el.read(dbfrom='nuccore',db='gene',linkname='nuccore_gene',id=id)
    ##     if '</eLinkResult>' not in xml:
    ##         raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=nuccore, dbto=gene, id="+id)
    ##     return xml
    ## 
    ## def elink_gene_to_nuccore(self,id):
    ##     xml = el.read(dbfrom='gene',db='nuccore',linkname='gene_nuccore',id=id)
    ##     if '</eLinkResult>' not in xml:
    ##         raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=gene, dbto=nuccore, id="+id)
    ##     return xml

