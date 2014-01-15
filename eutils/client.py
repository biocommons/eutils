__doc__ = """
>>> client = Client()
>>> pmr = client.pubmed.fetch_by_id(555)
>>> pmr.author1
Yoder RS
"""

default_tool =  __package__
default_email = 'reecehart+eutils@gmail.com'


# http://www.ncbi.nlm.nih.gov/books/NBK25499/table/chapter4.chapter4_table1/?report=objectonly

#import eutils.clients.pubmed
#import eutils.clients.refseq
#import eutils.clients.gene

class Client(object):
    def __init__(self, tool = default_tool, email = default_email):
        self.pubmed = eutils.clients.pubmed.Pubmed(tool=tool,email=email)
        self.refseq = eutils.clients.refseq.RefSeq(tool=tool,email=email)
        self.gene = eutils.clients.gene.Gene(tool=tool,email=email)
