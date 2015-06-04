import lxml.etree

from eutils.exceptions import EutilsError

class Base(object):

    """
    Root class for all xmlfacade classes.

    
    """
    
    _root_tag = None

    def __init__(self,xml_elem):
        if isinstance(xml_elem, str):
            # Eventually, we'll do this...
            # raise DeprecationWarning("Initializing instances with strings is deprecated; "
            #                          "please initialize with lxml _Element objects")
            self._xml = xml_elem
            self._xmlroot = lxml.etree.XML(xml_elem)
        elif isinstance(xml_elem, lxml.etree._Element):
            self._xml = None
            self._xmlroot = xml_elem
        else:
            raise RuntimeError("Cannot create object from type "+type(xml_elem).__name__)

        if self._root_tag is not None and self._root_tag != self._xmlroot.tag:
            raise EutilsError("XML for {} object must be a {} element (got {})".format(
                type(self).__name__, self._root_tag, self._xmlroot.tag))

    def __str__(self):
        return unicode(self).encode('utf-8')

    @classmethod
    def _validate_xml(xml):
        """validate the xml during initialization. Subclasses override this
        to apply any __init__-time validation of the incoming XML"""
        pass

