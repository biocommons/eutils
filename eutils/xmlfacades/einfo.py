import eutils.xmlfacades.base

class EInfo(eutils.xmlfacades.base.Base):

    def databases(self):
        return self._xmlroot.xpath('//DbName/text()')


class EInfoDB(eutils.xmlfacades.base.Base):
    
    pass
