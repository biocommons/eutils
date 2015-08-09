import lxml.etree

import eutils.xmlfacades.base
from eutils.xmlfacades.gbseq import GBSeq


class GBSet(eutils.xmlfacades.base.Base):

    _root_tag = 'GBSet'

    def __unicode__(self):
        return "GBSet({self.acv})".format(self=self)

    def __iter__(self):
        return (GBSeq(n) for n in self._xml_elem.iterfind('GBSeq'))


if __name__ == "__main__":
    import os
    import lxml.etree as le

    data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'tests', 'data')
    relpath = 'efetch.fcgi?db=nuccore&id=148536845&retmode=xml.xml'
    path = os.path.join(data_dir, relpath)
    gbset = GBSet(le.parse(path).getroot())
