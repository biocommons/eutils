xmlfacades
==========

These modules provide property-based access to data parsed from
eutilities XML replies.  

xmlfacades are initialized with an `lxml.etree._Element` and return a
class with methods appropriate for the XML node type.  Object
instantiation verifies that the correct type has been passed.  Classes
then provide properties to search or iterate as appropriate for that
node type, returning standard Python types or other xmlfacade
instances.

For consistency, class names correspond to XML node names, CapCased.
For example, the xmlfacade classes and corresponding xpath elements
for Entrezgene-Set replies are::

    xpath: /Entrezgene-Set/Entrezgene/Entrezgene_locus/Gene-commentary/Gene-commentary_products/Gene-commentary/Gene-commentary_genomic-coords
            ^              ^          ^                ^               ^                        ^               ^
    class:  EntrezgeneSet  Entrezgene EntrezgeneLocus  GeneCommentary  GeneCommentaryProducts   GeneCommentary  GeneCommentaryGenomicCoords

