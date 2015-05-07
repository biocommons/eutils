xmlfacades
==========

These modules provide property-based access to data parsed from
eutilities XML replies.  The classes take xml `str`s (deprecated) or
`lxml.etree._Element`s (newer mode), and return a class with methods
appropriate for the type. Object instantiation verifies that the
correct type has been passed.

The xmlfacade classes and corresponding xpath elements are:

/Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords
 ^             N^          ^                ^               ^                        ^               ^
 EntrezgeneSet  Entrezgene EntrezgeneLocus  GeneCommentary  GeneCommentaryProducts   GeneCommentary  GeneCommentaryGenomicCoords
