Using eutils
@@@@@@@@@@@@


Installation
############

::

  $ pip install eutils


A Quick Example
###############

::

    >>> import eutils.client
    
    # Initialize a client. This client handles all caching and query
    # throttling
    >>> ec = eutils.client.Client()
  
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
