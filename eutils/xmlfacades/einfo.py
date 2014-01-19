import eutils.xmlfacades.base

class EInfo(eutils.xmlfacades.base.Base):

    @property
    def databases(self):
        return sorted(self._xmlroot.xpath('//DbName/text()'))


class EInfoDB(eutils.xmlfacades.base.Base):
    
    @property
    def dbname(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/DbName/text()')[0]

    @property
    def menuname(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/MenuName/text()')[0]

    @property
    def description(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/Description/text()')[0]

    @property
    def dbbuild(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/DbBuild/text()')[0]

    @property
    def count(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/Count/text()')[0]

    @property
    def lastupdate(self):
        return self._xmlroot.xpath('/eInfoResult/DbInfo/LastUpdate/text()')[0]
