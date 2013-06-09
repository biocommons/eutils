import lxml.etree as le

class PubMedEntry(object):
    def __init__(self,xml):
        self.xml = xml
        self.doc = le.fromstring(xml)
        self.art = self.doc.find('PubmedArticle')

    @property
    def abstract(self):
        return self._get_text('PubmedArticle/MedlineCitation/Article/Abstract/AbstractText')

    @property
    def authors(self):
        # N.B. Citations may have 0 authors. e.g., pmid:7550356
        def _Last_FI(au):
            return au.find('LastName').text + ' ' + au.find('Initials').text
        return [ _Last_FI(au) for au
                 in self.doc.findall('PubmedArticle/MedlineCitation/Article/AuthorList/Author') ]

    @property
    def doi(self):
        return self._get_text('PubmedData/ArticleIdList/ArticleId[@IdType="doi"]')

    @property
    def issue(self):
        return self._get_text('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Issue')

    @property
    def jrnl(self):
        return ( self._get_text('PubmedArticle/MedlineCitation/Article/Journal/ISOAbbreviation')
                 or self._get_text('PubmedArticle/MedlineCitation/Article/Journal/Title') )
        return j

    @property
    def mesh_headings(self):
        return self.doc.xpath('PubmedArticle/MedlineCitation/MeshHeadingList/MeshHeading/DescriptorName/text()')

    @property
    def pages(self):
        return( self._get_text('PubmedArticle/MedlineCitation/Article/Pagination/MedlinePgn') )

    @property
    def pii(self):
        return self._get_text('PubmedData/ArticleIdList/ArticleId[@IdType="pii"]')

    @property
    def pmc(self):
        pmc = self._get_text('PubmedData/ArticleIdList/ArticleId[@IdType="pmc"]')
        return None if pmc is None else pmc[3:]

    @property
    def pmid(self):
        return self._get_text('PubmedArticle/MedlineCitation/PMID')

    @property
    def title(self):
        return self._get_text('PubmedArticle/MedlineCitation/Article/ArticleTitle')

    @property
    def volume(self):
        return self._get_text('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Volume')
    
    @property
    def year(self):
        y = self._get_text('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
        if y is None:
            # case applicable for pmid:9887384 (at least)
            y = self._get_text('PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/MedlineDate')[0:4]
        return y


    def as_dict(self):
        return {
            'pmid': self.pmid,
            'jrnl': self.jrnl,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'year': self.year,
            'authors': self.authors,
            'title': self.title,
            'mesh_headings': self.mesh_headings,
            'abstract': self.abstract,
            }

    ######################################################################
    ## INTERNAL CLASS FUNCTIONS
    def _get_node(self,tag):
        return self.doc.find(tag)
    def _get_text(self,tag):
        n = self._get_node(tag)
        return None if n is None else n.text
    def __str__(self):
        return( '%s (%s. %s, %s:%s)'.format(
            self.title, self.authors_str, self.jrnl, self.voliss, self.pages) )
