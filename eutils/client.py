from eutils.eutilsclient import EutilsClient
from eutils.xmlfacades.einfo import EInfo, EInfoDB
from eutils.xmlfacades.esearchresults import ESearchResults

class Client(object):
    def __init__(self):
        self._ec = EutilsClient()
        self.databases = self.einfo().databases()

    def einfo(self,db=None):
        if db is None:
            return EInfo( self._ec.einfo() )
        return EInfoDB( self._ec.einfo({'db':db}) )
        
    def esearch(self,db,term):
        return ESearchResults( self._ec.esearch({'db':db,'term':term}) )




    ############################################################################
    ## specific helpers
    def esearch_nuccore_by_ac(self,ac):
        # N.B. [accn] only works for current accessions
        xml = self.esearch(db='nuccore',term='%s[accn]' % (ac))
        if '<ErrorList><PhraseNotFound>' in xml:
            logging.debug("'%s[accn]' not found; trying unqualified search for unqualified query to pick up obsolete accession" % (ac))
            xml = self.esearch(db='nuccore',term=ac)
        if '</eSearchResult>' not in xml:
            raise LocusNCBIError("received malformed reply from NCBI for db=nuccore, ac="+ac)
        return ESearchResults(xml)

    def efetch_nuccore_by_id(self,id):
        xml = ef.read(db='nuccore',id=id,retmode='xml',rettype='gb')
        if '</GBSet>' not in xml:
            raise LocusNCBIError("received malformed reply from NCBI for db=nuccore, id="+id)
        return xml

    def efetch_nuccore_by_ac(self,ac):
        esr = ESearchResultParser( esearch_nuccore_by_ac(ac) )
        if esr.Count == 0:
            raise LocusNCBIError('{ac}: transcript not found'.format(ac=ac))
        if esr.Count > 1:
            raise LocusNCBIError("received %d replies for %s" % (esr.Count,ac))
        return efetch_nuccore_by_id( esr.IdList[0] )

    def esearch_gene_by_hgnc_name(self,name):
        query = 'human[orgn] AND {name}[symbol] AND {name}[titl] AND "current only"[Filter]'.format(name=name)
        xml = es.read(rettype='uilist',db='gene',term=query)
        if '</eSearchResult>' not in xml:
            raise LocusNCBIError("received malformed reply from NCBI for db=gene, query="+query)
        return xml

    def efetch_gene_by_id(self,id):
        xml = ef.read(db='gene',id=id)
        if '</Entrezgene-Set>' not in xml:
            raise LocusNCBIError("received malformed reply from NCBI db=gene, id="+id)
        return xml

    def efetch_gene_by_hgnc_name(self,name):
        esr = ESearchResultParser( esearch_gene_by_hgnc_name(name) )
        if esr.Count == 0:
            return None
        for id in esr.IdList:
            xml = efetch_gene_by_id( id )
            doc = le.XML(xml)
            reply_hgnc = doc.xpath('/Entrezgene-Set/Entrezgene/Entrezgene_gene/Gene-ref/Gene-ref_locus/text()')[0]
            if reply_hgnc == name:
                return xml
            logging.debug('queried for gene %s, skipped reply for gene %s' % (name,reply_hgnc))
        raise LocusNCBIError("NCBI search returned %d replies for %s, and none were for this gene!" % (
                esr.Count, name))

    def elink_nuccore_to_gene(self,id):
        xml = el.read(dbfrom='nuccore',db='gene',linkname='nuccore_gene',id=id)
        if '</eLinkResult>' not in xml:
            raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=nuccore, dbto=gene, id="+id)
        return xml

    def elink_gene_to_nuccore(self,id):
        xml = el.read(dbfrom='gene',db='nuccore',linkname='gene_nuccore',id=id)
        if '</eLinkResult>' not in xml:
            raise LocusNCBIError("received malformed elink reply from NCBI, dbfrom=gene, dbto=nuccore, id="+id)
        return xml

