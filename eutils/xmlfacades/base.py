import logging

import lxml.etree

from eutils.exceptions import EutilsError


logger = logging.getLogger(__name__)


class Base(object):

    """
    Root class for all xmlfacade classes.

    This class is instantiated only by subclasses.

    """
    
    _root_tag = None

    def __init__(self, xml_elem):
        if isinstance(xml_elem, str):
            # We're being called with a string in the old-school way
            self._xml = xml_elem
            self._xml_elem = lxml.etree.XML(xml_elem)
        elif isinstance(xml_elem, lxml.etree._Element):
            self._xml = None
            self._xml_elem = xml_elem
        else:
            raise EutilsError("Cannot create object from type " + type(xml_elem).__name__)

        self._validate_xml_elem()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def _validate_xml_elem(self):
        """Validate the xml during initialization.

        Returns True if the XML is valid.
        Returns False or throws `EutilsError`s on failure.

        By default, this method will check whether an
        _root_tag, if any, matches the xml tag of the element.

        At a minimum, subclasses should define _root_tag. 

        Alternatively, subclasses mayh override this method to apply
        more complex __init__-time validation of the incoming XML.

        """

        if self._root_tag is None:
            # raise EutilsError("_root_tag not defined for class {}".format(type(self).__name__))
            logger.warn("_root_tag not defined for class {}".format(type(self).__name__))
            return False

        if self._root_tag != self._xml_elem.tag:
            raise EutilsError("XML for {} object must be a {} element (got {})".format(
                type(self).__name__, self._root_tag, self._xml_elem.tag))

        return True
