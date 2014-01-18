import lxml.etree

class Base(object):

    def __init__(self,xml):
        self._xml = xml
        self._xmlroot = lxml.etree.XML(xml)
