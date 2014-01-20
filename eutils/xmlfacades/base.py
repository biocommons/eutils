import lxml.etree

class Base(object):

    def __init__(self,xml):
        self._xml = xml
        self._xmlroot = lxml.etree.XML(xml)

    @classmethod
    def _validate_xml(xml):
        """validate the xml during initialization. Subclasses override this
        to apply any __init__-time validation of the incoming XML"""
        pass
