import lxml.etree

from eutils.exceptions import EutilsError

class Base(object):

    def __init__(self,xml):
        if isinstance(xml, str):
            self._xml = xml
            self._xmlroot = lxml.etree.XML(xml)
        elif isinstance(xml, lxml.etree._Element):
            self._xml = None
            self._xmlroot = xml
        else:
            raise RuntimeError("Cannot create object from type "+type(xml).__name__)

        if self._root_tag is None:
            #TODO: Raise deprecation warning
            pass
        elif self._root_tag != self._xmlroot.tag:
            raise EutilsError("XML for {} object must be a {} element".format(
                type(self).__name__, self._root_tag))

    def __str__(self):
        return unicode(self).encode('utf-8')

    @classmethod
    def _validate_xml(xml):
        """validate the xml during initialization. Subclasses override this
        to apply any __init__-time validation of the incoming XML"""
        pass

