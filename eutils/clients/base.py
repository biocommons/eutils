"""
Interface to NCBI E-Utilities.
"""


class ClientBase(object):
    """DB searches one database type"""
    def __init__(self,db,email,tool):
        self._tool = __package__
        self._email = email
        self._tool = tool
        self._db = db
        self.base_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.url_fmt = self.base_url + '/{service}.fcgi?tool={tool}&email={email}&db={db}&rettype=xml'
        #&id={pmid}

    def esearch(query):
        """returns a set of ids for a query"""
        
    def efetch(ids):
        





if __name__ == "__main__":
    import doctest
    doctest.testmod()
