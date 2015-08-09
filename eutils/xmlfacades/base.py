import logging

import lxml.etree

from eutils.exceptions import EutilsError

logger = logging.getLogger(__name__)


class Base(object):
    """Root class for all xmlfacade classes.

    This class is instantiated only by subclasses.

    _root_tag must be defined by the subclass. It is used to validate
    the node type upon instantiation of the subclass.

    """

    _root_tag = None

    def __init__(self, xml_elem):
        if isinstance(xml_elem, lxml.etree._Element):
            self._xml = None
            self._xml_elem = xml_elem
        elif isinstance(xml_elem, str):
            logger.info("instantiating eutils xmlfacade with an xml string is deprecated; "
                        "consider passing the xml root instead (e.g., `lxml.etree.parse(xml).getroot()`)")
            self._xml = xml_elem
            self._xml_elem = lxml.etree.XML(xml_elem)
        else:
            raise EutilsError("Cannot create object from type " + type(xml_elem).__name__)

        if self._root_tag is None:
            raise EutilsError("_root_tag not defined for class {}".format(type(self).__name__))
        elif self._root_tag != self._xml_elem.tag:
            raise EutilsError("XML for {} object must be a {} element (got {})".format(
                type(self).__name__, self._root_tag, self._xml_elem.tag))

    def __str__(self):
        return unicode(self).encode('utf-8')
