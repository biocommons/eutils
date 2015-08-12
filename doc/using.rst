Using eutils
@@@@@@@@@@@@


Installation
############

The easiest way to install the eutils package is to use pre-build
Python package from PyPI, like so::

  $ pip install eutils

Consider using `virtualenvwrapper
<https://virtualenvwrapper.readthedocs.org/en/latest/>`_ or `pyvenv
<https://docs.python.org/3/library/venv.html>`_ to setup virtual
environments before installing eutils.

Code that relies on eutils should specify a version bracket to ensure
that eutils receives bug fixes but not updates that might break
compatibility.  In your package's setup.py::

  setup(
    ...
    install_requires = [
      'eutils>=0.1,<0.2',
    ],
    ...
    )

Alternatively, you may install from source; please see
:ref:`dev_install` for details.


Examples
########


Common setup
$$$$$$$$$$$$

Instantiating an eutils :class:`eutils.client.Client` is this easy::

    >>> import eutils
    
    # Initialize a client. This client handles all caching and query
    # throttling
    >>> ec = eutils.Client()
  

Fetching gene information
$$$$$$$$$$$$$$$$$$$$$$$$$

::

    # search for tumor necrosis factor genes
    # any valid NCBI query may be used
    >>> esr = ec.esearch(db='gene',term='tumor necrosis factor')
    
    # fetch one of those (gene id 7157 is human TNF)
    >>> egs = ec.efetch(db='gene',id=7157)
    
    # One may fetch multiple genes at a time. These are returned as an
    # EntrezgeneSet. We'll grab the first (and only) child, which returns
    # an instance of the Entrezgene class.
    >>> eg = egs.entrezgenes[0]
  
    # Easily access some basic information about the gene
    >>> eg.hgnc, eg.maploc, eg.description, eg.type, eg.genus_species
    ('TP53', '17p13.1', 'tumor protein p53', 'protein-coding', 'Homo sapiens')
  
    # get a list of genomic references
    >>> [str(r) for r in eg.references]
     ['GeneCommentary(acv=NC_000017.11,type=genomic,heading=Reference GRCh38.p2 Primary Assembly,label=Chromosome 17 Reference GRCh38.p2 Primary Assembly)',
      'GeneCommentary(acv=NG_017013.2,type=genomic,heading=None,label=RefSeqGene)',
      'GeneCommentary(acv=NC_018928.2,type=genomic,heading=Alternate CHM1_1.1,label=Chromosome 17 Alternate CHM1_1.1)']
    
    # Get all products defined on GRCh38
    >>> [p.acv for p in eg.references[0].products]
    [u'NM_001126112.2', u'NM_001276761.1', u'NM_000546.5',
    u'NM_001276760.1', u'NM_001126113.2', u'NM_001276695.1',
    u'NM_001126114.2', u'NM_001276696.1', u'NM_001126118.1',
    u'NM_001126115.1', u'NM_001276697.1', u'NM_001126117.1',
    u'NM_001276699.1', u'NM_001126116.1', u'NM_001276698.1']
  
    # As a sample, grab the first product defined on this reference (order is arbitrary)
    >>> mrna = eg.references[0].products[0]
    >>> str(mrna)
    'GeneCommentary(acv=NM_001126112.2,type=mRNA,heading=Reference,label=transcript variant 2)'
  
    # mrna.genomic_coords provides access to the exon definitions on this
    reference
  
    >>> mrna.genomic_coords.gi, mrna.genomic_coords.strand
    ('568815581', -1)
  
    >>> mrna.genomic_coords.intervals
    [(7687376, 7687549), (7676520, 7676618), (7676381, 7676402),
    (7675993, 7676271), (7675052, 7675235), (7674858, 7674970),
    (7674180, 7674289), (7673700, 7673836), (7673534, 7673607),
    (7670608, 7670714), (7668401, 7669689)]
  
    # and the mrna has a product, the resulting protein:
    >>> str(mrna.products[0])
    'GeneCommentary(acv=NP_001119584.1,type=peptide,heading=Reference,label=isoform a)'


Fetch PubMed information
$$$$$$$$$$$$$$$$$$$$$$$$

::

   # search pubmed by author
   >>> esr = c.esearch(db='pubmed', term='Nussbaum RL')

   # fetch all of them
   >>> paset = c.efetch(db='pubmed', id=esr.ids)
   
   # paset represents PubmedArticleSet, a collection of
   PubmedArticles. The major interface component is to iterate over
   PubmedArticles with constructs like `for pa in paset: ...`. We
   fetch the first PubmedArticle like this:
   >>> pa = iter(paset).next()
   
   PubmedArticle provides acccessors to essential data:
   >>> pa.title
   'High incidence of functional ion-channel abnormalities in a
   consecutive Long QT cohort with novel missense genetic variants of
   unknown significance.'
   
   >>> pa.authors
   [u'Steffensen AB', u'Refaat MM', u'David JP', u'Mujezinovic A',
   u'Calloe K', u'Wojciak J', u'Nussbaum RL', u'Scheinman MM',
   u'Schmitt N']
   
   >>> pa.jrnl, pa.volume, pa.issue, pa.year
   ('Sci Rep', '5', None, '2015')
   
   >>> pa.jrnl, pa.volume, pa.issue, pa.year, pa.pages
   ('Sci Rep', '5', None, '2015', '10009')
   
   >>> pa.pmid, pa.doi, pa.pmc
   ('26066609', '10.1038/srep10009', '4464365')
