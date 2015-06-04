xmlfacades
==========

These modules provide property-based access to data parsed from
eutilities XML replies.  

Older classes, which take `str`s of entire XML documents, are
deprecated.  The primary problem with this approach is that it didn't
easily allow multiple replies per request. The secondary problem was
that all descendant attributes were accessed from the node
corresponding to the document root.

Newer classes take `lxml.etree._Element`s and return a class with
methods appropriate for the XML node type.  That is, parsing is done
by the client, not by the class.  Object instantiation verifies that
the correct type has been passed.  Classes then provide properties to
search or iterate as appropriate for that node type, returning
standard Python types or other xmlfacade instances.  When completed,
there will be classes that correspond to all major eutils reply types.

For consistency, class names correspond to XML node names, CapCased.
For example, the xmlfacade classes and corresponding xpath elements
for Entrezgene-Set replies are:

xpath: /Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords
        ^              ^          ^                ^               ^                        ^               ^
class:  EntrezgeneSet  Entrezgene EntrezgeneLocus  GeneCommentary  GeneCommentaryProducts   GeneCommentary  GeneCommentaryGenomicCoords


